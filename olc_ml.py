"""Kural vs ML vs birleşik kıyası.  Kullanım: python olc_ml.py

Protokol: ML dev'de eğitilir (C ve Belirsiz eşiği dev üzerinde çapraz doğrulamayla seçilir), test'te ölçülür.
Ek olarak tüm veri üzerinde 5-katlı çapraz doğrulama (ML için ayar sızıntısı yok, kural için yok sayılır).
"""
import sys

import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_predict

from mailsinif import kural, olcum
from mailsinif.ml import MLSiniflandirici, _boru, _metin, birlesik_fn

sys.stdout.reconfigure(encoding="utf-8")
dev, test = olcum.bol(olcum.yukle())

# --- dev üzerinde C ve eşik seçimi (yalnızca dev) ---
X = [_metin(d["konu"], d["govde"]) for d in dev]
y = [d["kategori"] for d in dev]
cv = StratifiedKFold(5, shuffle=True, random_state=0)
en_iyi = None
for C in (1, 10, 100):
    P = cross_val_predict(_boru(C), X, y, cv=cv, method="predict_proba")
    siniflar = sorted(set(y))
    for esik in (0.0, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6):
        tah = [siniflar[int(np.argmax(p))] if p.max() >= esik else "Belirsiz" for p in P]
        belirsiz = sum(t == "Belirsiz" for t in tah) / len(tah)
        emin = [(g, t) for g, t in zip(y, tah) if t != "Belirsiz"]
        if not emin:
            continue
        acc = sum(g == t for g, t in emin) / len(emin)
        if belirsiz <= 0.17 and (en_iyi is None or acc > en_iyi[0]):
            en_iyi = (acc, C, esik, belirsiz)
acc, C, esik, bel = en_iyi
print(f"Dev-CV ile seçilen: C={C}, eşik={esik} (dev-CV emin doğruluk %{100*acc:.1f}, Belirsiz %{100*bel:.1f})\n")

ml = MLSiniflandirici(C, esik).egit(dev)
sonuc = {
    "Kural": olcum.olc(test, kural.siniflandir),
    "ML": olcum.olc(test, ml.siniflandir),
    "Birleşik (önce kural, emin değilse ML)": olcum.olc(test, birlesik_fn(ml)),
}
print("## TEST kıyası (n=%d)\n" % len(test))
print("| Yöntem | Emin doğruluk | Genel doğruluk | Belirsiz oranı | Acil P/R |\n|---|---|---|---|---|")
for ad, s in sonuc.items():
    print(f"| {ad} | %{100*s['dogruluk_emin']:.1f} | %{100*s['dogruluk_genel']:.1f} | %{100*s['belirsiz_orani']:.1f} | "
          f"%{100*s['acil_precision']:.0f}/%{100*s['acil_recall']:.0f} |")
print()
for ad in ("ML", "Birleşik (önce kural, emin değilse ML)"):
    print(olcum.yazdir("TEST: " + ad, sonuc[ad]), "\n")

# --- tüm veri üzerinde 5-katlı CV (ML, seçilen C/eşik) ---
tum = olcum.yukle()
Xa = [_metin(d["konu"], d["govde"]) for d in tum]
ya = [d["kategori"] for d in tum]
accs, bels = [], []
for tohum in range(3):
    P = cross_val_predict(_boru(C), Xa, ya, cv=StratifiedKFold(5, shuffle=True, random_state=tohum), method="predict_proba")
    sinif = sorted(set(ya))
    tah = [sinif[int(np.argmax(p))] if p.max() >= esik else "Belirsiz" for p in P]
    emin = [(g, t) for g, t in zip(ya, tah) if t != "Belirsiz"]
    accs.append(sum(g == t for g, t in emin) / len(emin))
    bels.append(sum(t == "Belirsiz" for t in tah) / len(tah))
print(f"Tüm veri, 5-katlı CV x3 tohum (ML): emin doğruluk %{100*np.mean(accs):.1f} (±{100*np.std(accs):.1f}), "
      f"Belirsiz %{100*np.mean(bels):.1f}")
