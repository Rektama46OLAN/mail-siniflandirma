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

## [2026-09-30] Temiz Windows'ta `.exe` denemesi (Arda)
- Durum: `dist/MailSiniflandirma` yalnızca PATH'ten Python çıkarılarak simüle edilmiş ortamda denendi; Python'suz gerçek makinede denenmedi.
- Sonraki adım: Windows Sandbox veya temiz bir bilgisayarda klasörü açıp çalıştırmak; sonucu (SmartScreen uyarısı, ilk açılış süresi, hata) bildirmek. `python derle.py` ile paket yeniden üretilebilir.
- Bağlam: teslimat/KURULUM.md, gecmislog "Faz 4b".

## [2026-09-30] Teklif aşaması (henüz başlamadı, karar Arda'da)
- Durum: Kanıt projesi bitti. Teklif metni, fiyatlandırma ve hedef müşteri listesi konuşulmadı; KVKK/veri işleme değerlendirmesi (opsiyonel LLM katmanı için) yapılmadı.
- Sonraki adım: Arda konuyu açınca teklif planı (kanıt raporundaki "söylenebilir / söylenemez" bölümü çıkış noktası) ve ilk pilot müşteri kurgusu.
- Bağlam: reports/2026-09-30-kanit-raporu.md, ArdaOS Inbox/Dump/2026-09-30-eposta-siniflandirma-proje-raporu.md.
