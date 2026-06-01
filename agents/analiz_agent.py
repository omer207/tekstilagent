from agents.base import call_ollama
from tools.calculator import uretim_depo_orani, ortalama_kimyasal_tuketim, ortalama_oee

ANALIZ_PROMPT = """
Sen bir veri analisti. Aşağıdaki hesaplanmış metrikleri kullanarak kullanıcıya analiz sun.

Üretim/Depo oranı: {oran}
Ortalama kimyasal tüketim (kg/gün): {kimyasal}
Ortalama OEE: {oee}

Kullanıcı sorusu: {question}

Yorumlarını veriye dayandır, trendleri vurgula.
"""

def analiz_yap(question: str) -> str:
    oran = uretim_depo_orani()
    kimyasal = ortalama_kimyasal_tuketim()
    oee = ortalama_oee()
    
    prompt = ANALIZ_PROMPT.format(
        oran=oran,
        kimyasal=kimyasal,
        oee=oee,
        question=question
    )
    return call_ollama("llama3", prompt)