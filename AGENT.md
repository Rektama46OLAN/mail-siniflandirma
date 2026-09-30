# AGENT.md

## Proje
**Mail Sınıflandırma** — E-ticaret satıcıları için gelen e-postaları kategoriye ayıran, API'siz çalışan Python masaüstü aracı (kanıt projesi).
Python, kural tabanlı + TF-IDF/lojistik regresyon (scikit-learn), masaüstü GUI, Excel rapor (openpyxl)

## const.md — değişmez gerçekler
Projedeki değişmez gerçekler `const.md`'de tutulur. Oradaki maddeler verili kabul
edilir; bir kararı/gerçeği kontrol etmek gerektiğinde önce `const.md`'ye bakılır,
değiştirmeden önce Arda'ya sorulur.

## notes.md — çalışan tasarım dokümanı
Fikirler, faz planı, tasarım detayları ve henüz açık maddeler `notes.md`'de tutulur.
`const.md` karara bağlanmış olanı, `notes.md` üzerinde çalışılanı tutar.

## reports/ klasörü
Ek raporlar `reports/` klasörüne konur. Arda'nın alışkanlığı: bir rapor / analiz /
çıktı üretildiğinde `reports/` altına atmak.

- Rapor aranması gerektiğinde ilk `reports/` klasörüne bak.
- Yeni bir rapor üretince ayrı belirtilmedikçe `reports/` altına kaydet.

## gecmis.md — yarım kalan işler
Bir iş yarıda kalırsa `gecmis.md`'ye not bırakılır (durum, sonraki adım, bağlam).
Amaç: hiçbir iş yarım kalmasın.

- Her oturum başında `gecmis.md` kontrol edilir; açık maddeler bitmeden yeni işe geçilmez.
- Madde tamamlanınca `gecmis.md`'den silinir, özeti `gecmislog.md`'ye taşınır.

## gecmislog.md — çalışma logu
Rekt çalışırken notlarını `gecmislog.md`'ye düşer. **Buraya düşen loglar silinmez.**
`gecmis.md` temizlendikçe kapanan maddeler burada birikir — "temizlik" bilgi kaybı
değildir, kapanan her şeyin kalıcı kaydı burasıdır.

## Git
- **Push yalnızca Arda açıkça "push yap" dediğinde yapılır.** "Commit'le" demesi
  push isteği değildir; commit atılır ve orada durulur.
- **Commit mesajları açıklayıcı olur.** Özet satırından sonra boş satır bırakılıp
  gövde yazılır: ne değişti, neden değişti, yol boyunca hangi sorun çözüldü.
- **Sır dosyaları asla commit'lenmez.** Token, şifre ve bağlantı URL'i git'e girmez.

## Çalışma Notları
- Kararı Arda verir; teknoloji, mimari ve kapsam onun onayından geçer.
- Varsayma — sor. Over-engineering yok.
- Kod cevabı: Yaklaşım → Neden → Kod → Açıklama → Dikkat edilecekler.

## Not: CLAUDE.md ↔ AGENT.md senkronizasyonu
Bu iki dosya her zaman aynı içeriğe sahip olmalı (yalnızca ilk satırdaki başlık farklı).

- `CLAUDE.md` içinde bir değişiklik yaparsam, aynısını `AGENT.md` dosyasına da uygula.
- `AGENT.md` içinde bir değişiklik yaparsam, aynısını `CLAUDE.md` dosyasına da uygula.
