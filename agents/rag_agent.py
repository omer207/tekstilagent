from agents.base import call_ollama
from agents.summarizer_agent import summarize_question
from core.memory import search_long_term_memory

RAG_PROMPT = """
Sen bir tekstil boyahane asistanısın. Aşağıdaki konuşma geçmişi, ilgili dokümanlar ve kullanıcı sorusuna göre cevap ver.

İLGİLİ DOKÜMANLAR:
{context}

KULLANICI SORUSU (ÖZETLENMİŞ):
{summarized_question}

CEVAP:
"""

def rag_cevapla(original_question: str, chat_history: str = "") -> str:
    summarized = summarize_question(original_question)
    docs = search_long_term_memory(summarized, k=4)
    context = "\n---\n".join(docs) if docs else "İlgili doküman bulunamadı."
    prompt = RAG_PROMPT.format(context=context, summarized_question=summarized)
    return call_ollama("llama3", prompt)