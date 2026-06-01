from agents.base import call_ollama
from tools.alert_checker import sicaklik_anomalileri

UYARI_PROMPT = """
Sen bir üretim izleme uzmanısın. Aşağıdaki makine anomalilerini değerlendir.

ANOMALİLER:
{anomaliler}

Kullanıcı sorusu: {question}

Anomali varsa açıkça uyar, yoksa "Herhangi bir anormallik tespit edilmedi" de.
"""

def uyari_kontrol(question: str) -> str:
    anomaliler = sicaklik_anomalileri()
    if anomaliler:
        anomali_metni = "\n".join([f"- Makine {a['makine_id']}: {a['zaman']} - {a['ak_sicaklik']}°C" for a in anomaliler])
    else:
        anomali_metni = "Anomali yok."
    
    prompt = UYARI_PROMPT.format(anomaliler=anomali_metni, question=question)
    return call_ollama("llama3", prompt)