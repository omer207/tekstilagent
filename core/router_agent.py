from agents.base import call_ollama
from pathlib import Path

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "router.md"
with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    ROUTER_PROMPT = f.read()

def router_decision(question: str) -> str:
    prompt = ROUTER_PROMPT.format(question=question)
    decision = call_ollama("llama3", prompt).strip().lower()
    # Geçerli cevaplar listesi
    valid = {"rapor", "analiz", "uyari", "planlama", "rag"}
    # Eğer model geçersiz bir şey dönerse varsayılan "rapor"
    return decision if decision in valid else "rapor"