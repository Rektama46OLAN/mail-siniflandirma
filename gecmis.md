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

## [2026-09-30] Faz 1b: etiket onayı (Arda bekleniyor)
- Durum: Subagent B bitti. Bağımsız etiket yazarla %93,5 uyuştu (257/275); 18 kategori ve 5 acil uyuşmazlığı `reports/2026-09-30-etiket-denetimi.md`'de.
- Sonraki adım: Arda o listedeki maillere bakıp doğru etiketi söyler; düzeltmeler `data/uretim/`'e işlenir, set dondurulur. Ondan sonra Faz 2 (kural baseline) — onaysız etiketle kod yazmaya başlanabilir ama ölçüm onaydan sonra yeniden alınır.
- Bağlam: `data/denetim/` (kor.jsonl, anahtar.json, etiket_b.jsonl). Yazarın etiketi ile bağımsız etiket farklıysa hangisi doğru, Arda karar verir.
