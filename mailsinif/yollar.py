"""Dosya yolları: geliştirmede proje klasörü, paketlenmiş .exe'de gömülü kaynak klasörü."""
import os
import sys

PAKETLI = getattr(sys, "frozen", False)
# salt okunur kaynaklar (eğitim verisi, önceden eğitilmiş model): .exe'de PyInstaller'ın açtığı klasör
KAYNAK = sys._MEIPASS if PAKETLI else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def kullanici_klasoru() -> str:
    """Yazılabilir kullanıcı verisi (ör. düzeltmeler, yeniden eğitilmiş model). .exe'de %APPDATA%, geliştirmede proje klasörü."""
    if PAKETLI:
        yol = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "MailSiniflandirma")
        os.makedirs(yol, exist_ok=True)
        return yol
    return KAYNAK
