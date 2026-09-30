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

## [2026-09-30] Faz 1b: etiket onayı — TAMAMLANDI
- Ne yapıldı: Arda uyuşmazlık raporunu inceledi ve etiketleri doğru buldu; yazarın etiketleri korundu, düzeltme yapılmadı. Set donduruldu (275 mail).
- Yol boyunca çıkanlar: Arda'nın cevabı "hepsi doğru gibi duruyor" idi; bunu yazar etiketlerinin onayı olarak yorumladım (bağımsız etiket değil). Yanlışsa bildirilir, set yeniden açılır.
- Dokunulan dosyalar: reports/2026-09-30-etiket-denetimi.md, data/denetim/*

## [2026-09-30] Faz 2: kural tabanlı baseline — TAMAMLANDI
- Ne yapıldı: `mailsinif/` (metin, kural, ölçüm) ve `olc_kural.py`. Dev/test bölünmesiyle ölçüldü; test'te emin maillerde %76,9, genel %70,9, Belirsiz %17,0, Acil %76/%92.
- Yol boyunca çıkanlar: İlk atış (ayarsız) emin maillerde %61,5/%68,6 idi. Dev hatalarına bakılarak ayar yapılınca dev %81,7, test %76,9: ~5 puan şişme. Ana hatalar: "sipariş" kelimesi şikayet/fatura mailini çekiyor, "hediye/kampanya" meşru müşteri mailini Spam'e atıyor. Şikayet test recall %17: dolaylı anlatım kalıpla yakalanmıyor. Çalıştırma sırasında sunucu tarafı izin sınıflandırıcısı art arda 5 kez "no verdict" verdi; geçici, sonra çalıştı.
- Dokunulan dosyalar: mailsinif/*, olc_kural.py, reports/2026-09-30-kural-ilk-atis.md, reports/2026-09-30-kural-baseline.md, notes.md

## [2026-09-30] Faz 3: ML kıyası — TAMAMLANDI
- Ne yapıldı: `mailsinif/ml.py` (TF-IDF kelime+karakter n-gram + lojistik regresyon, Belirsiz olasılık eşiği), `olc_ml.py`. Aynı dev/test bölünmesinde kural %76,9, ML %71,2, birleşik %77,2 (emin doğruluk); ML tüm veride 5-katlı CV %77,3.
- Yol boyunca çıkanlar: scikit-learn kurulu değildi, pip ile kuruldu (requirements.txt eklendi). Eşik ızgarasında yüksek eşik tüm mailleri Belirsiz yapıp sıfıra bölme hatası verdi; boş "emin" kümesi atlandı. Fark kural/birleşik arasında n=141'de gürültü sınırında.
- Dokunulan dosyalar: mailsinif/ml.py, olc_ml.py, requirements.txt, reports/2026-09-30-kural-ml-kiyas.md, notes.md

## [2026-09-30] Yöntem kararı ve doğruluk-kapsam eğrisi — TAMAMLANDI
- Ne yapıldı: Arda birleşik yöntemi onayladı (const.md'ye girdi); gerçek mail yerine sentetikte kalınacak. Öğrenme eğrisi (55→220 mail: doğruluk %72,4→%76,7, Belirsiz %34→%12,7) ve `olc_egri.py` ile doğruluk-kapsam eğrisi çıkarıldı.
- Yol boyunca çıkanlar: %90 doğruluk ≈%55 kapsam demek; eski hedef çifti (>%90 ve ≤%15-20 Belirsiz) birlikte sağlanamıyor. Eşikler ölçüm verisinde tarandığından eğri hafif iyimser.
- Dokunulan dosyalar: const.md, notes.md, olc_egri.py, reports/2026-09-30-dogruluk-kapsam-egrisi.md

## [2026-09-30] Doğruluk hedefi kararı — TAMAMLANDI
- Ne yapıldı: Arda "%80'ini ayırır, ayırdığının %85'i doğru" senaryosunu seçti; const.md'ye çalışma noktası (kural güveni 0,5, ML eşiği 0,5) ve Tkinter kararı yazıldı.
- Yol boyunca çıkanlar: const.md'de eski "Arayüz" maddesi yeni maddeyle çiftlendi; tek maddede birleştirildi.
- Dokunulan dosyalar: const.md

## [2026-09-30] Faz 4: masaüstü pencere ve Excel rapor — TAMAMLANDI
- Ne yapıldı: `mailsinif/oku.py` (.eml/.mbox/.csv, HTML gövde temizleme), `motor.py` (birleşik motor, model kaydet/yükle), `rapor.py` (Özet, Mailler, Kontrol listesi + açılır liste, Okunamayanlar), `uygulama.py` (Tkinter; arka plan iş parçacığı, ilerleme, renkli tablo, Excel'e kaydet), `test_akis.py`, `ornek_mailler/yeni_mailler.csv` (16 elle yazılmış, eğitim setinde olmayan mail), README.md.
- Yol boyunca çıkanlar: Test klasörüne bilerek konan bozuk CSV okunamayanlara düştü, akış durmadı. Elle yazılan 16 yeni mailde 15/16 doğru (küçük örnek ve kuralları bilerek yazıldığı için iyimser; tek hata "iade parası yatmadı", Şikayet yerine Fatura, zaten sınırda bir mail). Pencere yalnızca programatik olarak sürüldü, düğme tıklaması/dosya diyalogları elle denenmedi.
- Dokunulan dosyalar: mailsinif/oku.py, motor.py, rapor.py, uygulama.py, test_akis.py, ornek_mailler/, README.md, requirements.txt, .gitignore

## [2026-09-30] Faz 4b: Windows paketleme — TAMAMLANDI
- Ne yapıldı: `mailsinif/yollar.py` (geliştirme/paketli yol ayrımı, kullanıcı verisi için %APPDATA%), `derle.py` (modeli eğitip PyInstaller onedir ile `dist/MailSiniflandirma/` üretir, 169 MB), `uygulama.py`'ye `--test KLASOR CIKTI.xlsx` modu, `teslimat/KURULUM.md` (SmartScreen adımlı müşteri yönergesi). Arda imzasız + onedir yaklaşımını kabul etti.
- Yol boyunca çıkanlar: Yollar `__file__`'a göre hesaplanıyordu, `.exe`'de bozulurdu; `sys._MEIPASS`'e alındı. PATH'ten Python çıkarılmış ortamda `.exe --test` 16 mailden Excel üretti (çıkış kodu 0); pencere açıldı ("Mail Sınıflandırma"). İlk çalıştırma 19 sn, ikinci 2 sn (soğuk başlangıç/Defender taraması); müşteriye yönergede belirtildi, isteğe bağlı açılış ekranı yapılabilir.
- Doğrulanmayanlar: gerçek temiz makine/Windows Sandbox denemesi, kod imzası, Mac.
- Ek (aynı gün, Arda'nın isteğiyle): Açılış ekranı eklendi. Gecikme pencere açılmadan önce scikit-learn içe aktarılırken oluşuyordu, bu yüzden Tkinter içi bir ekran işe yaramazdı; PyInstaller `--splash` (Python başlamadan bootloader gösterir) kullanıldı, görsel `assets/acilis.png` (Pillow ile üretildi), `uygulama.py` pencere açılınca `pyi_splash.close()` çağırıyor; model de pencere açılır açılmaz arka planda yükleniyor. Ekran görüntüsüyle doğrulandı: soğuk açılışta ekran 0,26 sn'de görünüp ana pencere 28,5 sn'de açıldı (ekran kapandı); sıcak açılışta 0,15 sn / 1,6 sn.
- Dokunulan dosyalar: mailsinif/yollar.py, olcum.py, uygulama.py, derle.py, teslimat/KURULUM.md, notes.md, .gitignore
