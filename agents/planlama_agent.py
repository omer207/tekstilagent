from agents.base import call_ollama
from tools.data_loader import load_musteri_talepleri

PLANLAMA_PROMPT = """
Sen bir üretim planlama uzmanısın. Aşağıdaki müşteri taleplerine göre günlük üretim planı öner.

TALEPLER:
{talepler}

Kullanıcı sorusu: {question}

Teslim tarihlerine göre önceliklendir, tonajları belirt.
"""

def planlama_yap(question: str) -> str:
    talepler = load_musteri_talepleri()
    if talepler.empty:
        talep_metni = "Bugün için hiç müşteri talebi yok."
    else:
        talep_metni = talepler.to_string(index=False)
    
    prompt = PLANLAMA_PROMPT.format(talepler=talep_metni, question=question)
    return call_ollama("llama3", prompt)