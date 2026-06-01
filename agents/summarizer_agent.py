from agents.base import call_ollama

SUMMARIZE_PROMPT = """
Sen bir metin özetleme uzmanısın. Kullanıcının sorusunu en fazla 2 cümlede özetle.
Sadece ana isteği koru. Gereksiz detayları çıkar.
Token sayısını mümkün olduğunca azalt.

Kullanıcı sorusu: {question}

Özet:
"""

def summarize_question(question: str) -> str:
    prompt = SUMMARIZE_PROMPT.format(question=question)
    return call_ollama("phi3", prompt).strip()