import pandas as pd
from pathlib import Path

# CSV dosyalarının bulunduğu ana klasör (data/csv veya doğrudan data)
# Eğer CSV'leriniz doğrudan "data" klasöründeyse aşağıdaki satırı kullanın:
# DATA_DIR = Path(__file__).parent.parent / "data"
# Eğer "data/csv" altındaysa:
DATA_DIR = Path(__file__).parent.parent / "data" / "csv"

def load_depo_girdileri():
    path = DATA_DIR / "depo_girdileri.csv"
    if not path.exists():
        # Geçici boş DataFrame döndür, hata vermesin
        return pd.DataFrame(columns=["tarih", "tonaj", "aciklama"])
    return pd.read_csv(path, parse_dates=["tarih"])

def load_sevkiyatlar():
    path = DATA_DIR / "sevkiyatlar.csv"
    if not path.exists():
        return pd.DataFrame(columns=["tarih", "tonaj", "musteri"])
    return pd.read_csv(path, parse_dates=["tarih"])

def load_makine_verileri():
    path = DATA_DIR / "makine_verileri.csv"
    if not path.exists():
        return pd.DataFrame(columns=["zaman", "makine_id", "ak_sicaklik"])
    return pd.read_csv(path, parse_dates=["zaman"])

def load_musteri_talepleri():
    path = DATA_DIR / "musteri_talepleri.csv"
    if not path.exists():
        return pd.DataFrame(columns=["tarih", "musteri", "urun", "tonaj", "teslim_tarihi"])
    return pd.read_csv(path, parse_dates=["tarih", "teslim_tarihi"])

def load_erp_tuketim():
    path = DATA_DIR / "erp_tuketim.csv"
    if not path.exists():
        return pd.DataFrame(columns=["tarih", "kimyasal_kg", "su_m3", "enerji_kwh"])
    return pd.read_csv(path, parse_dates=["tarih"])

def load_tuketimler():
    """Parti bazlı tüketimler (opsiyonel)"""
    path = DATA_DIR / "tuketimler.csv"
    if not path.exists():
        return pd.DataFrame(columns=["parti_no", "toplam_su_lt", "elektrik_kwh", "buhar_kg", "kimyasal_kg", "boya_kg"])
    return pd.read_csv(path)

def load_partiler():
    path = DATA_DIR / "partiler.csv"
    if not path.exists():
        return pd.DataFrame(columns=["parti_no", "is_emri", "makine_id", "recete_no", "baslama_zamani", "bitis_zamani", "gercek_sure_dk", "kumas_kg"])
    return pd.read_csv(path, parse_dates=["baslama_zamani", "bitis_zamani"])

def load_receteler():
    path = DATA_DIR / "receteler.csv"
    if not path.exists():
        return pd.DataFrame(columns=["recete_no", "islem_adi", "teorik_sure_dk", "adim_sayisi", "t_kimyasal", "t_boya"])
    return pd.read_csv(path)