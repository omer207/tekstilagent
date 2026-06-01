import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from tools.data_loader import (
    load_depo_girdileri, load_sevkiyatlar, load_makine_verileri,
    load_musteri_talepleri, load_tuketimler
)
from tools.calculator import uretim_depo_orani, ortalama_kimyasal_tuketim
from tools.alert_checker import sicaklik_anomalileri
from core.memory import short_memory, search_long_term_memory
from agents.base import call_ollama

def build_context(question: str) -> str:
    """İhtiyaç duyulan tüm verileri topla ve metin haline getir"""
    context = []
    
    # Depo ve sevkiyat (rapor için)
    depo = load_depo_girdileri()
    sevk = load_sevkiyatlar()
    if not depo.empty:
        context.append(f"Depo girişleri (son 3 gün):\n{depo.tail(3).to_string(index=False)}")
    if not sevk.empty:
        context.append(f"Sevkiyatlar (son 3 gün):\n{sevk.tail(3).to_string(index=False)}")
    
    # Analiz metrikleri
    oran = uretim_depo_orani()
    kimyasal = ortalama_kimyasal_tuketim()
    context.append(f"Üretim/Depo oranı: {oran:.2f}")
    context.append(f"Ortalama kimyasal tüketim: {kimyasal:.1f} kg/gün")
    
    # Uyarı (sadece anomali varsa)
    anomaliler = sicaklik_anomalileri()
    if anomaliler:
        context.append(f"MAKİNE UYARILARI: {len(anomaliler)} adet anormal sıcaklık tespit edildi.")
        for a in anomaliler[:2]:
            context.append(f"- Makine {a['makine_id']}: {a['ak_sicaklik']}°C")
    
    # Planlama (müşteri talepleri)
    talepler = load_musteri_talepleri()
    if not talepler.empty:
        context.append(f"Müşteri talepleri (özet):\n{talepler[['musteri','tonaj','teslim_tarihi']].to_string(index=False)}")
    
    # RAG (vektör DB'den ilgili belgeler)
    rag_docs = search_long_term_memory(question, k=2)
    if rag_docs:
        context.append("İlgili dokümanlar:\n" + "\n---\n".join(rag_docs[:2]))
    
    # Kısa süreli hafıza (son 2 konuşma)
    chat_context = short_memory.get_context()
    if chat_context:
        context.append("Son konuşmalar:\n" + chat_context)
    
    return "\n\n".join(context)

MAIN_PROMPT = """
Sen bir tekstil boyahane asistanısın. Aşağıda mevcut veriler ve kullanıcı sorusu var.
Verilere dayanarak kullanıcıya doğrudan, net ve yardımcı bir cevap ver.
Sayısal verileri vurgula, gerekirse liste yap. Gereksiz detaya girme.

MEVCUT VERİLER:
{context}

KULLANICI SORUSU:
{question}

CEVAP:
"""

def run_agentic_flow(question: str) -> str:
    context = build_context(question)
    prompt = MAIN_PROMPT.format(context=context, question=question)
    answer = call_ollama("llama3", prompt)
    # Hafızaya kaydet
    short_memory.add(question, answer)
    return answer