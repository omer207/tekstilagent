from agents.base import call_ollama
from tools.data_loader import load_depo_girdileri, load_sevkiyatlar

RAPOR_PROMPT = """
Sen bir raporlama uzmanısın. Aşağıdaki depo giriş ve sevkiyat verilerini kullanarak kullanıcıya özet bir rapor sun.

DEPO GİRİŞİ (tonaj): {depo_giris}
SEVKİYAT (tonaj): {sevkiyat}

Kullanıcı sorusu: {question}

Lütfen verileri tablo veya madde işaretleriyle düzenli bir şekilde sun.
"""

def raporla(question: str) -> str:
    depo = load_depo_girdileri()
    sevk = load_sevkiyatlar()
    depo_toplam = depo["tonaj"].sum() if not depo.empty else 0
    sevk_toplam = sevk["tonaj"].sum() if not sevk.empty else 0
    
    prompt = RAPOR_PROMPT.format(
        depo_giris=depo_toplam,
        sevkiyat=sevk_toplam,
        question=question
    )
    return call_ollama("llama3", prompt)