# Geçmiş Log

Rekt buraya çalışırken notlarını düşer.

**Buraya düşen loglar silinmez.** `gecmis.md` temizlendikçe kapanan maddeler burada birikir.
Yani "temizlik" bilgi kaybı anlamına gelmez — `gecmis.md` sadece açık işleri tutar,
kapanan her şeyin kalıcı kaydı buradadır.

Yarım kalan işler buraya değil `gecmis.md`'ye yazılır.

## Format

```
## [TARİH] İş başlığı — TAMAMLANDI
- Ne yapıldı: tek satır özet
- Yol boyunca çıkanlar: karşılaşılan sorun ve çözümü (varsa)
- Dokunulan dosyalar: ...
```

---

## Log

## [2026-09-30] Faz 0: planlama iskeleti ve GitHub — TAMAMLANDI
- Ne yapıldı: proje-planlama iskeleti kuruldu, karar özeti notes.md/const.md'ye işlendi, public repo açıldı (Rektama46OLAN/mail-siniflandirma).
- Yol boyunca çıkanlar: PowerShell 5.1'de `git commit -F -` here-string ile çalışmadı; mesaj `-m $msg` ile verildi. `gh repo create` push'u başarılı olsa da stderr çıktısını hata gibi gösteriyor.
- Dokunulan dosyalar: CLAUDE.md, AGENT.md, notes.md, const.md, gecmis.md, gecmislog.md, .gitignore

## [2026-09-30] Faz 1a: test maili üretimi — TAMAMLANDI
- Ne yapıldı: 8 Sonnet subagent kategori başına yapay mail yazdı; toplam 275 mail (7×35 + Belirsiz 30), `data/uretim/*.jsonl`.
- Yol boyunca çıkanlar: Hiçbir ajan çıktısını doğrulamamıştı. Şema kontrolünde `soru.jsonl` 26. satırda eksik tırnak (`kisilik":"kisa",kategori"`) bulundu ve elle düzeltildi; ajan "fazla alanı çıkardım" derken bozmuştu. Ajan raporlarına güvenmeden dosya ayrıştırılmalı.
- Dokunulan dosyalar: data/uretim/*.jsonl
