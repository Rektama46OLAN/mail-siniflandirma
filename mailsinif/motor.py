"""Birleşik sınıflandırma motoru (const.md): önce kural (emin ise), değilse ML. Modeli eğitir/saklar/yükler."""
import os

import joblib

from . import kural, olcum
from .ml import MLSiniflandirici

KURAL_GUVEN = 0.5   # const.md: çalışma noktası ~%80 kapsam / ~%85 doğruluk
ML_ESIK = 0.5
KONTROL_ESIGI = 0.6  # bunun altındaki güven "kontrol et" listesine düşer
MODEL_YOLU = os.path.join(olcum.KOK, "model", "ml.joblib")


class Motor:
    def __init__(self, ml: MLSiniflandirici):
        self.ml = ml

    @classmethod
    def egit(cls, veri=None, kaydet=True):
        veri = veri if veri is not None else olcum.yukle()
        ml = MLSiniflandirici(C=100, esik=ML_ESIK).egit(veri)
        if kaydet:
            os.makedirs(os.path.dirname(MODEL_YOLU), exist_ok=True)
            joblib.dump(ml, MODEL_YOLU)
        return cls(ml)

    @classmethod
    def yukle_veya_egit(cls):
        """Kaydedilmiş model varsa yükler, yoksa eğitim verisinden eğitir (saniyeler sürer)."""
        if os.path.exists(MODEL_YOLU):
            try:
                return cls(joblib.load(MODEL_YOLU))
            except Exception:
                pass
        return cls.egit()

    def siniflandir(self, konu: str, govde: str) -> dict:
        k = kural.siniflandir(konu, govde)
        if k["kategori"] != "Belirsiz" and k["guven"] >= KURAL_GUVEN:
            sonuc, yontem = k, "kural"
        else:
            sonuc, yontem = self.ml.siniflandir(konu, govde), "ml"
        return {"kategori": sonuc["kategori"], "guven": sonuc["guven"], "acil": sonuc["acil"], "yontem": yontem,
                "kontrol": sonuc["kategori"] == "Belirsiz" or sonuc["guven"] < KONTROL_ESIGI}
