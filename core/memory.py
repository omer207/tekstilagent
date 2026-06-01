import json
from pathlib import Path
from collections import deque
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings


MEMORY_DIR = Path(__file__).parent.parent / "memory_data"
CHAT_HISTORY_FILE = MEMORY_DIR / "chat_history.json"
VECTOR_DB_DIR = MEMORY_DIR / "chroma_db"

embeddings = OllamaEmbeddings(model="llama3")
vectorstore = Chroma(
    persist_directory=str(VECTOR_DB_DIR),
    embedding_function=embeddings,
    collection_name="textile_memory"
)

class ShortTermMemory:
    def __init__(self, max_length=5):
        self.max_length = max_length
        self.messages = deque(maxlen=max_length)
        self._load()

    def add(self, user: str, assistant: str):
        self.messages.append({"user": user, "assistant": assistant})
        self._save()

    def get_context(self) -> str:
        if not self.messages:
            return ""
        context = []
        for msg in self.messages:
            context.append(f"Kullanıcı: {msg['user']}\nAsistan: {msg['assistant']}")
        return "\n---\n".join(context)

    def _save(self):
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(list(self.messages), f, ensure_ascii=False, indent=2)

    def _load(self):
        if CHAT_HISTORY_FILE.exists():
            with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.messages.extend(data[-self.max_length:])

short_memory = ShortTermMemory()

def search_long_term_memory(query: str, k: int = 3):
    results = vectorstore.similarity_search(query, k=k)
    return [doc.page_content for doc in results]

def add_to_long_term_memory(text: str, metadata: dict = None):
    from langchain_core.documents import Document
    doc = Document(page_content=text, metadata=metadata or {})
    vectorstore.add_documents([doc])
    vectorstore.persist()