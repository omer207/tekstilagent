from agents.base import call_ollama

AGGREGATOR_PROMPT = """
Sen bir tekstil boyahane asistanısın. Aşağıda bir uzman ajanın verdiği cevap var.
Bu cevabı kullanıcıya doğal, anlaşılır ve profesyonel bir dille ilet.

UZMANIN CEVABI:
{agent_response}

KULLANICININ SORUSU:
{original_question}

LÜTFEN:
- Cevabı düzenle, gereksiz tekrarları çıkar
- Sayısal verileri vurgula
- Eksik bilgi varsa belirt
- Kibar ve yardımcı ol

DÜZENLENMİŞ CEVAP:
"""

def aggregate_response(agent_response: str, original_question: str) -> str:
    if not agent_response or len(agent_response) < 10:
        return "Üzgünüm, bu konuda yeterli bilgiye sahip değilim."
    prompt = AGGREGATOR_PROMPT.format(
        agent_response=agent_response[:3000],
        original_question=original_question
    )
    return call_ollama("llama3", prompt)