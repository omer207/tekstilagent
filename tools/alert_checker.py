from .data_loader import load_makine_verileri

def sicaklik_anomalileri(esik=85):
    df = load_makine_verileri()
    if df.empty or "ak_sicaklik" not in df.columns:
        return []
    anormal = df[df["ak_sicaklik"] > esik]
    if not anormal.empty:
        return anormal[["zaman", "makine_id", "ak_sicaklik"]].to_dict("records")
    return []