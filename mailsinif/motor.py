"""Birleşik sınıflandırma motoru (const.md): önce kural (emin ise), değilse ML. Modeli eğitir/saklar/yükler.

İki model dosyası: pakete gömülü `model/ml.joblib` (derle.py üretir) ve kullanıcının düzeltmelerle yeniden eğittiği
`<kullanıcı klasörü>/kullanici_model/ml.joblib`. Yüklerken kullanıcı modeli önceliklidir.
"""
import os

import joblib

from . import kural, olcum
from .ml import MLSiniflandirici
from .yollar import kullanici_klasoru

KURAL_GUVEN = 0.5   # const.md: çalışma noktası ~%80 kapsam / ~%85 doğruluk
ML_ESIK = 0.5
KONTROL_ESIGI = 0.6  # bunun altındaki güven "kontrol et" listesine düşer
MODEL_YOLU = os.path.join(olcum.KOK, "model", "ml.joblib")
KULLANICI_MODEL_YOLU = os.path.join(kullanici_klasoru(), "kullanici_model", "ml.joblib")
DUZELTME_AGIRLIGI = 3.0  # müşterinin düzelttiği mail, sentetik eğitim mailinden daha değerli sayılır


class Motor:
    def __init__(self, ml: MLSiniflandirici):
        self.ml = ml

    @classmethod
    def egit(cls, veri=None, kaydet=True, yol=MODEL_YOLU):
        veri = veri if veri is not None else olcum.yukle()
        ml = MLSiniflandirici(C=100, esik=ML_ESIK).egit(veri)
        if kaydet:
            os.makedirs(os.path.dirname(yol), exist_ok=True)
            joblib.dump(ml, yol)
        return cls(ml)

    @classmethod
    def yukle_veya_egit(cls):
        """Kullanıcı modeli, yoksa gömülü model; ikisi de yoksa/bozuksa eğitim verisinden eğitir (saniyeler sürer)."""
        for yol in (KULLANICI_MODEL_YOLU, MODEL_YOLU):
            if os.path.exists(yol):
                try:
                    return cls(joblib.load(yol))
                except Exception:
                    pass
        return cls.egit()

    @classmethod
    def duzeltmelerle_yeniden_egit(cls, duzeltmeler: list[dict]):
        """Temel eğitim verisi + müşteri düzeltmeleriyle eğitir, kullanıcı modeli olarak kaydeder."""
        veri = olcum.yukle() + [{**d, "agirlik": DUZELTME_AGIRLIGI} for d in duzeltmeler]
        return cls.egit(veri, kaydet=True, yol=KULLANICI_MODEL_YOLU)

    @staticmethod
    def sifirla():
        """Kullanıcı modelini siler; sonraki açılışta gömülü (fabrika) model kullanılır."""
        if os.path.exists(KULLANICI_MODEL_YOLU):
            os.remove(KULLANICI_MODEL_YOLU)

    def siniflandir(self, konu: str, govde: str) -> dict:
        k = kural.siniflandir(konu, govde)
        if k["kategori"] != "Belirsiz" and k["guven"] >= KURAL_GUVEN:
            sonuc, yontem = k, "kural"
        else:
            sonuc, yontem = self.ml.siniflandir(konu, govde), "ml"
        return {"kategori": sonuc["kategori"], "guven": sonuc["guven"], "acil": sonuc["acil"], "yontem": yontem,
                "kontrol": sonuc["kategori"] == "Belirsiz" or sonuc["guven"] < KONTROL_ESIGI}
