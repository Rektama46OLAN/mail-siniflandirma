"""ML sınıflandırıcı: TF-IDF (kelime + karakter n-gram) + lojistik regresyon.

Belirsiz hem eğitimde bir sınıf hem de olasılık eşiğinin altında düşülen karar. Acil kural kalıbından gelir
(Acil için etiketli ayrı model kurulmadı; kural zaten recall %92-100).
"""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion, Pipeline

from . import kural
from .metin import normalle


def _metin(konu: str, govde: str) -> str:
    return normalle(konu) + " ||| " + normalle(govde)


def _boru(C: float) -> Pipeline:
    return Pipeline([
        ("tfidf", FeatureUnion([
            ("kelime", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, min_df=1)),
            ("kar", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), sublinear_tf=True, min_df=2)),
        ])),
        ("lr", LogisticRegression(C=C, max_iter=2000, class_weight="balanced")),
    ])


class MLSiniflandirici:
    def __init__(self, C: float = 10.0, esik: float = 0.0):
        self.C, self.esik = C, esik
        self.boru = _boru(C)

    def egit(self, veri: list[dict]):
        self.boru.fit([_metin(d["konu"], d["govde"]) for d in veri], [d["kategori"] for d in veri],
                      lr__sample_weight=[d.get("agirlik", 1.0) for d in veri])
        return self

    def olasiliklar(self, veri: list[dict]):
        return self.boru.predict_proba([_metin(d["konu"], d["govde"]) for d in veri])

    @property
    def siniflar(self):
        return list(self.boru.classes_)

    def siniflandir(self, konu: str, govde: str) -> dict:
        p = self.boru.predict_proba([_metin(konu, govde)])[0]
        i = int(np.argmax(p))
        kat = self.siniflar[i] if p[i] >= self.esik else "Belirsiz"
        return {"kategori": kat, "guven": round(float(p[i]), 3), "acil": kural.acil_mi(konu, govde)}


def birlesik_fn(ml: MLSiniflandirici, kural_guven: float = 0.5):
    """Önce kural (emin ise), değilse ML."""
    def f(konu, govde):
        k = kural.siniflandir(konu, govde)
        if k["kategori"] != "Belirsiz" and k["guven"] >= kural_guven:
            return k
        return ml.siniflandir(konu, govde)
    return f
