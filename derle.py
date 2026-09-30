"""Windows .exe klasörünü üretir (PyInstaller, onedir).  Kullanım: python derle.py

1) Modeli eğitim verisinden eğitip model/ml.joblib olarak kaydeder (pakete gömülür).
2) PyInstaller ile dist/MailSiniflandirma/ klasörünü kurar; içine eğitim verisi, model ve örnek mailler girer.
Çıktı klasörünü zip'leyip müşteriye verin. Müşteride Python gerekmez.
"""
import os
import shutil
import subprocess
import sys

from mailsinif.motor import Motor

kok = os.path.dirname(os.path.abspath(__file__))
os.chdir(kok)

print("Model eğitiliyor…")
Motor.egit(kaydet=True)

for k in ("build", "dist"):
    shutil.rmtree(k, ignore_errors=True)

sep = os.pathsep
komut = [
    sys.executable, "-m", "PyInstaller", "--noconfirm", "--onedir", "--windowed",
    "--name", "MailSiniflandirma",
    "--splash", f"assets{os.sep}acilis.png",  # Python başlamadan gösterilir; uygulama pencereyi açınca kapatır
    "--add-data", f"model{sep}model",
    "--add-data", f"data{os.sep}uretim{sep}data{os.sep}uretim",
    "--add-data", f"ornek_mailler{sep}ornek_mailler",
    "--exclude-module", "matplotlib", "--exclude-module", "IPython", "--exclude-module", "pytest",
    "uygulama.py",
]
print(" ".join(komut))
subprocess.run(komut, check=True)
boyut = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk("dist") for f in fs) / 1e6
print(f"\nHazır: dist/MailSiniflandirma/MailSiniflandirma.exe ({boyut:.0f} MB toplam)")
