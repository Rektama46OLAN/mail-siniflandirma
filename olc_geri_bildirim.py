"""Geri bildirim simülasyonu: müşteri "Kontrol listesi"ndeki maillere doğru kategoriyi veriyor, model yeniden eğitiliyor.

Görülmemiş test setinde (dokunulmaz) doğruluk her turda ölçülür. Başlangıç modeli dev'in yarısıyla eğitilir
(müşterinin maili eğitim setinden farklı olduğu durumu taklit eder); kalan dev mailleri müşterinin gelen kutusu gibi
tur tur gelir. Her turda yalnızca sistemin "kontrol et" dediği mailler düzeltilir (gerçek kullanımdaki gibi).
Kullanım: python olc_geri_bildirim.py
"""
import random
import sys

import numpy as np

from mailsinif import olcum
from mailsinif.motor import DUZELTME_AGIRLIGI, Motor

sys.stdout.reconfigure(encoding="utf-8")
dev, test = olcum.bol(olcum.yukle())
TUR, BATCH = 3, 22
TOHUMLAR = range(8)


def olc(motor):
    s = olcum.olc(test, motor.siniflandir)
    return s["dogruluk_emin"], s["dogruluk_genel"], s["belirsiz_orani"]


sonuc = {t: [] for t in range(TUR + 1)}
duzeltilen = {t: [] for t in range(1, TUR + 1)}
for tohum in TOHUMLAR:
    r = random.Random(tohum)
    havuz = dev[:]
    r.shuffle(havuz)
    temel, akis = havuz[: len(havuz) // 2], havuz[len(havuz) // 2:]
    egitim = list(temel)
    motor = Motor.egit(egitim, kaydet=False)
    sonuc[0].append(olc(motor))
    for t in range(1, TUR + 1):
        parti = akis[(t - 1) * BATCH: t * BATCH]
        sonuclar = [motor.siniflandir(m["konu"], m["govde"]) for m in parti]
        kontrol = [m for m, s in zip(parti, sonuclar) if s["kontrol"]]
        duzeltilen[t].append(len(kontrol))
        egitim += [{**m, "agirlik": DUZELTME_AGIRLIGI} for m in kontrol]  # müşteri doğru kategoriyi verir
        motor = Motor.egit(egitim, kaydet=False)
        sonuc[t].append(olc(motor))

print(f"Simülasyon: başlangıç {len(temel)} mail, her turda {BATCH} yeni mail, {len(list(TOHUMLAR))} rastgele bölünme, test n={len(test)}\n")
print("| Tur | Düzeltilen mail (tur başına) | Emin doğruluk | Genel doğruluk | Belirsiz oranı |\n|---|---|---|---|---|")
for t in range(TUR + 1):
    a = np.array(sonuc[t])
    d = f"{np.mean(duzeltilen[t]):.1f}" if t else "-"
    print(f"| {t} | {d} | %{100*a[:,0].mean():.1f} (±{100*a[:,0].std():.1f}) | %{100*a[:,1].mean():.1f} | %{100*a[:,2].mean():.1f} |")
