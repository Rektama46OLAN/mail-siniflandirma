# Geçmiş — Yarım Kalan İşler

Bir iş yarıda kalırsa buraya not bırakılır. **Amaç: hiçbir iş yarım kalmasın.**
Her oturum başında bu dosya kontrol edilir; buradaki maddeler bitmeden yeni işe geçilmez.

Bir madde tamamlandığında buradan silinir ve özeti `gecmislog.md`'ye taşınır.

## Format

```
## [TARİH] İş başlığı
- Durum: nerede kalındı
- Sonraki adım: ne yapılacak
- Bağlam: ilgili dosyalar / kararlar
```

---

## Açık işler

## [2026-09-30] Faz 3: ML kıyası
- Durum: Başlamadı. Faz 2 kapandı (kural baseline test'te emin maillerde %76,9).
- Sonraki adım: scikit-learn kurulumu kontrolü, TF-IDF + lojistik regresyon, aynı dev/test bölünmesi, olasılık eşiğiyle Belirsiz; kural/ML/birleşik tablosu `reports/`'a.
- Bağlam: notes.md Faz 3, reports/2026-09-30-kural-baseline.md. Gerçek rakam test sütunudur.
