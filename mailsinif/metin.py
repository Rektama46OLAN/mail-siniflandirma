"""Metin normalleştirme: Türkçe küçük harf + aksan sadeleştirme (yazım hatalı/aksansız maillere dayanıklı)."""
import re

_KATLA = str.maketrans("çğıöşüâîû", "cgiosuaiu")


def normalle(s: str) -> str:
    s = s.replace("İ", "i").replace("I", "ı").lower().translate(_KATLA)
    return re.sub(r"\s+", " ", s).strip()
