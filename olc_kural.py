"""Kural tabanlı baseline'ı dev ve test bölümlerinde ölçer.  Kullanım: python olc_kural.py [--hatalar dev|test]"""
import sys

from mailsinif import kural, olcum

sys.stdout.reconfigure(encoding="utf-8")

dev, test = olcum.bol(olcum.yukle())
sd, st = olcum.olc(dev, kural.siniflandir), olcum.olc(test, kural.siniflandir)
print(olcum.yazdir("DEV", sd))
print()
print(olcum.yazdir("TEST", st))

if "--rapor" in sys.argv:
    from mailsinif.kural import KATEGORILER as K
    kisa = [k.split(" /")[0] for k in K]
    satir = ["\n## Karışıklık matrisi, TEST (satır = gerçek, sütun = tahmin)\n",
             "| gerçek \\ tahmin | " + " | ".join(kisa) + " |", "|---|" + "---|" * len(K)]
    for g, gk in zip(K, kisa):
        satir.append(f"| {gk} | " + " | ".join(str(st["karisiklik"][(g, t)]) for t in K) + " |")
    print("\n".join(satir))

if "--hatalar" in sys.argv:
    hedef = sd if sys.argv[sys.argv.index("--hatalar") + 1] == "dev" else st
    print("\n## Hatalar")
    for d, t in hedef["hatalar"]:
        print(f"- {d['id']}: gerçek={d['kategori']} tahmin={t['kategori']} | {d['konu']} | {d['govde'][:110]!r}")
