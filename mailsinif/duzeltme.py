"""Müşteri düzeltmeleri: Excel "Kontrol listesi"ndeki "Doğru kategori" sütununu okur, saklar, modeli yeniden eğitir."""
import json
import os

from openpyxl import load_workbook

from .kural import KATEGORILER
from .yollar import kullanici_klasoru

DUZELTME_DOSYASI = os.path.join(kullanici_klasoru(), "duzeltmeler.jsonl")


def excel_oku(yol: str) -> tuple[list[dict], list[str]]:
    """Döner: (düzeltmeler, uyarılar). Boş bırakılan satırlar atlanır; geçersiz kategori uyarı olur."""
    wb = load_workbook(yol, read_only=True, data_only=True)
    if "Kontrol listesi" not in wb.sheetnames:
        raise ValueError("Bu dosyada 'Kontrol listesi' sayfası yok. Programın ürettiği bir Excel raporu seçin.")
    satirlar = wb["Kontrol listesi"].iter_rows(values_only=True)
    baslik = [str(b or "") for b in next(satirlar, [])]
    try:
        i_konu, i_dogru = baslik.index("Konu"), next(i for i, b in enumerate(baslik) if b.startswith("Doğru kategori"))
        i_onizleme, i_acil = baslik.index("Önizleme"), baslik.index("Acil")
    except (ValueError, StopIteration):
        raise ValueError("'Kontrol listesi' sayfasının sütunları tanınmadı; dosya değiştirilmiş olabilir.")
    i_tam = baslik.index("Tam metin") if "Tam metin" in baslik else None

    duzeltmeler, uyarilar = [], []
    for n, r in enumerate(satirlar, 2):
        dogru = (r[i_dogru] or "").strip() if len(r) > i_dogru and r[i_dogru] else ""
        if not dogru:
            continue
        if dogru not in KATEGORILER:
            uyarilar.append(f"Satır {n}: '{dogru}' geçerli bir kategori değil, atlandı.")
            continue
        govde = (r[i_tam] if i_tam is not None and len(r) > i_tam and r[i_tam] else None) or (r[i_onizleme] or "")
        duzeltmeler.append({"konu": str(r[i_konu] or ""), "govde": str(govde), "kategori": dogru,
                            "acil": bool(r[i_acil])})
    wb.close()
    return duzeltmeler, uyarilar


def kayitli() -> list[dict]:
    if not os.path.exists(DUZELTME_DOSYASI):
        return []
    with open(DUZELTME_DOSYASI, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def sil():
    if os.path.exists(DUZELTME_DOSYASI):
        os.remove(DUZELTME_DOSYASI)


def kaydet(yeni: list[dict]) -> tuple[list[dict], int]:
    """Yeni düzeltmeleri mevcutlarla birleştirir (aynı konu+metin ise sonuncusu geçerli). Döner: (tümü, yeni eklenen sayısı)."""
    tum = {(d["konu"], d["govde"]): d for d in kayitli()}
    once = len(tum)
    for d in yeni:
        tum[(d["konu"], d["govde"])] = d
    os.makedirs(os.path.dirname(DUZELTME_DOSYASI), exist_ok=True)
    with open(DUZELTME_DOSYASI, "w", encoding="utf-8") as f:
        for d in tum.values():
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    return list(tum.values()), len(tum) - once
