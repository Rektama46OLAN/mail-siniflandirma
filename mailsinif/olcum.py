"""Ölçüm: veri yükleme, dev/test ayrımı, doğruluk, Belirsiz oranı, karışıklık matrisi."""
import glob
import json
import os
import re
from collections import Counter

from .kural import KATEGORILER
from .yollar import KAYNAK as KOK


def yukle(klasor: str = "data/uretim") -> list[dict]:
    satirlar = []
    for f in sorted(glob.glob(os.path.join(KOK, klasor, "*.jsonl"))):
        with open(f, encoding="utf-8") as fh:
            satirlar += [json.loads(l) for l in fh if l.strip()]
    return satirlar


def bol(veri: list[dict]) -> tuple[list[dict], list[dict]]:
    """Dev = çift numaralı id, test = tek numaralı id (kural yalnızca dev'e bakılarak ayarlanır)."""
    dev, test = [], []
    for d in veri:
        (dev if int(re.search(r"(\d+)$", d["id"]).group(1)) % 2 == 0 else test).append(d)
    return dev, test


def olc(veri: list[dict], tahmin_fn) -> dict:
    tahminler = [tahmin_fn(d["konu"], d["govde"]) for d in veri]
    n = len(veri)
    gercek = [d["kategori"] for d in veri]
    tah = [t["kategori"] for t in tahminler]
    dogru = sum(g == t for g, t in zip(gercek, tah))
    emin = [(g, t) for g, t in zip(gercek, tah) if t != "Belirsiz"]
    emin_dogru = sum(g == t for g, t in emin)
    belirsiz_tah = sum(t == "Belirsiz" for t in tah)
    tp = sum(d["acil"] and t["acil"] for d, t in zip(veri, tahminler))
    fp = sum((not d["acil"]) and t["acil"] for d, t in zip(veri, tahminler))
    fn = sum(d["acil"] and not t["acil"] for d, t in zip(veri, tahminler))
    conf = Counter(zip(gercek, tah))
    return {
        "n": n,
        "dogruluk_genel": dogru / n,
        "dogruluk_emin": emin_dogru / len(emin) if emin else 0.0,
        "belirsiz_orani": belirsiz_tah / n,
        "acil_precision": tp / (tp + fp) if tp + fp else 0.0,
        "acil_recall": tp / (tp + fn) if tp + fn else 0.0,
        "kategori_basina": {
            k: {
                "n": gercek.count(k),
                "recall": conf[(k, k)] / gercek.count(k) if gercek.count(k) else 0.0,
                "precision": conf[(k, k)] / tah.count(k) if tah.count(k) else 0.0,
            }
            for k in KATEGORILER
        },
        "karisiklik": conf,
        "hatalar": [(d, t) for d, t in zip(veri, tahminler) if d["kategori"] != t["kategori"]],
    }


def yazdir(ad: str, s: dict) -> str:
    o = [f"## {ad} (n={s['n']})",
         f"- Genel doğruluk (Belirsiz de bir sınıf): %{100*s['dogruluk_genel']:.1f}",
         f"- Emin olunan maillerde doğruluk (tahmin≠Belirsiz): %{100*s['dogruluk_emin']:.1f}",
         f"- Belirsiz'e düşen oran: %{100*s['belirsiz_orani']:.1f}",
         f"- Acil: precision %{100*s['acil_precision']:.0f}, recall %{100*s['acil_recall']:.0f}",
         "", "| Kategori | n | recall | precision |", "|---|---|---|---|"]
    for k, v in s["kategori_basina"].items():
        o.append(f"| {k} | {v['n']} | %{100*v['recall']:.0f} | %{100*v['precision']:.0f} |")
    return "\n".join(o)
