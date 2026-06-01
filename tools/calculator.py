from .data_loader import load_depo_girdileri, load_sevkiyatlar, load_tuketimler, load_partiler, load_receteler

def uretim_depo_orani():
    depo = load_depo_girdileri()
    sevk = load_sevkiyatlar()
    toplam_depo = depo["tonaj"].sum() if not depo.empty else 0
    toplam_sevk = sevk["tonaj"].sum() if not sevk.empty else 0
    return toplam_sevk / toplam_depo if toplam_depo else 0

def ortalama_kimyasal_tuketim():
    t = load_tuketimler()
    if t.empty or "kimyasal_kg" not in t.columns:
        return 0
    return t["kimyasal_kg"].mean()

def ortalama_oee():
    partiler = load_partiler()
    receteler = load_receteler()
    if partiler.empty or receteler.empty:
        return 0.0
    # Ortak kolon adı "recete_no" olduğunu varsayıyoruz
    df = partiler.merge(receteler, left_on="recete_no", right_on="recete_no", how="inner")
    if df.empty:
        return 0.0
    df["teorik_sure"] = df["teorik_sure_dk"]
    df["verim"] = df["teorik_sure"] / df["gercek_sure_dk"]
    # Kalite faktörü varsayılan 0.95
    df["oee"] = df["verim"] * 0.95
    return df["oee"].mean()