"""Birleşik yöntemin doğruluk-kapsam eğrisi.  Kullanım: python olc_egri.py

Kapsam = Belirsiz'e düşmeyen mail oranı; doğruluk = kapsanan maillerdeki doğruluk.
İki düğme taranır: kural güven eşiği (kg) ve ML olasılık eşiği (mt). Sonuç Pareto sınırıdır.
(1) ML dev'de eğitilir, test'te ölçülür. (2) Tüm veride 5-katlı CV (ML her katta yeniden eğitilir).
Not: eşikler ölçüm verisi üzerinde tarandığı için eğri betimleyicidir; üretimde eşik ayrı veriyle seçilmelidir.
"""
import sys

import numpy as np
from sklearn.model_selection import StratifiedKFold

from mailsinif import kural, olcum
from mailsinif.ml import _boru, _metin

sys.stdout.reconfigure(encoding="utf-8")
KG = (0.0, 0.3, 0.5, 0.7, 0.9)
MT = (0.0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8)


def kural_on(veri):
    return [kural.siniflandir(d["konu"], d["govde"]) for d in veri]


def tara(veri, kur, ml, sinif):
    P = ml.predict_proba([_metin(d["konu"], d["govde"]) for d in veri])
    y = [d["kategori"] for d in veri]
    sonuc = []
    for kg in KG:
        for mt in MT:
            tah = []
            for k, p in zip(kur, P):
                if k["kategori"] != "Belirsiz" and k["guven"] >= kg:
                    tah.append(k["kategori"])
                else:
                    tah.append(sinif[int(p.argmax())] if p.max() >= mt else "Belirsiz")
            e = [(g, t) for g, t in zip(y, tah) if t != "Belirsiz"]
            if e:
                sonuc.append((len(e) / len(y), sum(g == t for g, t in e) / len(e), kg, mt))
    return sonuc


def sinir(sonuc):
    """Pareto: kapsam arttıkça doğruluk düşer; her kapsam düzeyi için en iyi doğruluk."""
    sonuc = sorted(sonuc, key=lambda t: (-t[0], -t[1]))
    en_iyi, out = -1, []
    for kap, acc, kg, mt in sonuc:
        if acc > en_iyi:
            out.append((kap, acc, kg, mt))
            en_iyi = acc
    return sorted(out)


def yaz(baslik, sonuc):
    print(f"## {baslik}\n\n| Kapsam | Belirsiz | Doğruluk (kapsananda) | kural güven eşiği | ML eşiği |\n|---|---|---|---|---|")
    for kap, acc, kg, mt in sinir(sonuc):
        print(f"| %{100*kap:.0f} | %{100*(1-kap):.0f} | %{100*acc:.1f} | {kg} | {mt} |")
    print()


dev, test = olcum.bol(olcum.yukle())
ml = _boru(100).fit([_metin(d["konu"], d["govde"]) for d in dev], [d["kategori"] for d in dev])
yaz("Test seti (ML dev'de eğitildi, n=%d)" % len(test), tara(test, kural_on(test), ml, list(ml.classes_)))

tum = olcum.yukle()
X = np.array([_metin(d["konu"], d["govde"]) for d in tum])
y = np.array([d["kategori"] for d in tum])
kur = kural_on(tum)
toplam = []
for tohum in range(3):
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=tohum).split(X, y):
        m = _boru(100).fit(X[tr], y[tr])
        toplam.append(tara([tum[i] for i in te], [kur[i] for i in te], m, list(m.classes_)))
# katlar üzerinde ortalama (aynı (kg, mt) çiftleri sırayla üretildiği için indeksle)
ort = []
for i in range(len(toplam[0])):
    if all(len(t) > i and t[i][2:] == toplam[0][i][2:] for t in toplam):
        ort.append((np.mean([t[i][0] for t in toplam]), np.mean([t[i][1] for t in toplam]), *toplam[0][i][2:]))
yaz("Tüm veri, 5-katlı CV x3 tohum (n=%d, kural dev'de ayarlanmış olduğundan hafif iyimser)" % len(tum), ort)
