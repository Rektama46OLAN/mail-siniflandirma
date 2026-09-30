# Kanıt raporu: e-posta sınıflandırma (2026-09-30)

Teklif aşamasında kullanılacak rakamlar ve bunların **nerede bittiği**. Tüm ölçümler yapay (sentetik) Türkçe
e-ticaret mailleriyle yapıldı; gerçek müşteri maili kullanılmadı.

## 1. Ne yapıyor
Bir klasördeki `.eml` / `.mbox` / `.csv` mailleri okur, her maili 8 kategoriden birine ayırır (Sipariş / Talep, Fatura / Ödeme,
Şikayet / Sorun, Soru / Bilgi, Belge / Evrak, Otomatik bildirim, Reklam / Spam, Belirsiz), Acil işareti koyar ve Excel'e yazar.
Emin olmadığı mailleri "Belirsiz" veya "kontrol et" diye insana bırakır. Bilgisayarda çalışır, internete bağlanmaz, mailleri değiştirmez.
Yöntem: önce kural tabanlı sınıflandırıcı, emin değilse TF-IDF + lojistik regresyon (const.md).

## 2. Nasıl ölçüldü
- **Veri:** 275 yapay mail (7 kategori × 35, Belirsiz 30). 8 ayrı yazar (subagent) farklı kişiliklerle yazdı: kısa, uzun, hatalı, kızgın, resmi, emojili vb.
- **Etiketler:** Yazarın etiketi; ayrı bir bağımsız etiketleyici etiketi görmeden aynı mailleri etiketledi, uyum %93,5 (257/275); Arda uyuşmazlıkları inceleyip yazarın etiketlerini onayladı.
- **Ölçüm:** 5-katlı çapraz doğrulama × 5 tekrar (her turda model, ölçülen maili görmeden eğitilir). Kurallar geliştirme sırasında verinin yarısına (dev) bakılarak ayarlandığı için rakamlar hafif iyimserdir.
- **Çalışma noktası:** Kural güveni 0,5, ML olasılığı 0,5 (const.md).

## 3. Sonuçlar (çapraz doğrulama, n=275)

| Ölçü | Değer |
|---|---|
| Sınıflandırılan mail oranı (kapsam) | **%80** (Belirsiz %19,6) |
| Sınıflandırılanların doğruluğu | **%84,5** (±4,8 puan turlar arası) |
| Genel doğruluk (Belirsiz de bir sınıf) | %74,1 |
| Acil işareti | precision %78, recall %95 |

Doğruluk-kapsam ödünleşimi (Belirsiz oranı arttıkça doğruluk artar, `2026-09-30-dogruluk-kapsam-egrisi.md`):
Belirsiz %44 → doğruluk ~%90; Belirsiz %27 → ~%86; Belirsiz %13 → ~%83. Yani "%90 doğruluk" ancak maillerin yaklaşık yarısı insana bırakılınca elde edilir.

### Kategori bazında

| Kategori | Gerçek mail | Doğru bulunan | Doğru çıkan | Belirsiz'e düşen |
|---|---|---|---|---|
| Sipariş / Talep | 35 | %57 | %73 | %26 |
| Fatura / Ödeme | 35 | %83 | %71 | %14 |
| Şikayet / Sorun | 35 | %46 | %81 | %37 |
| Soru / Bilgi | 35 | %75 | %75 | %9 |
| Belge / Evrak | 35 | %98 | %94 | %2 |
| Otomatik bildirim | 35 | %97 | %100 | %1 |
| Reklam / Spam | 35 | %78 | %96 | %15 |
| Belirsiz | 30 | %57 | %32 | %57 |

**Güçlü:** Belge, Otomatik bildirim, Spam, Fatura, Soru. **Zayıf:** Şikayet ve Sipariş. Şikayetlerin %37'si, Siparişlerin %26'sı "Belirsiz"e düşüyor
(dolaylı anlatım: "paket ezilmiş geldi", "bu üçüncü kez yazıyorum"). Bunlar kaçırılmıyor, insana bırakılıyor; ama sistem bunlarda en az iş yapıyor.

## 4. "Kullandıkça öğrenir" iddiası: ölçülen gerçek
Excel'deki Kontrol listesi müşteri düzeltmelerini toplar; pencereden yüklenince model yeniden eğitilir (düzeltmeler 3 kat ağırlıklı).
Simülasyon (8 rastgele bölünme, müşteri yalnızca "kontrol et" dediğimiz mailleri düzeltiyor, görülmemiş 141 mailde ölçüm):
her turda ~7 düzeltme; 3 tur (~20 düzeltme) sonrası genel doğruluk %65,1 → %66,5, Belirsiz oranı %32,5 → %30,9, sınıflandırılanların doğruluğu ~%85 sabit.
**Yani iyileşme gerçek ama yavaş** (20 düzeltme ≈ +1,4 puan). Asıl değeri, müşterinin kendi kelime dağarcığına uyum olabilir; bu sentetik veriyle ölçülemez.

## 5. Sınırlar (teklifte dürüstçe söylenmeli)
- **Sentetik veri.** Gerçek maillerde doğruluk düşebilir. Tek üretim kaynağı (aynı model ailesi) kalıplaşma riski taşır. Gerçek mail testi yapılmadı (Arda'nın gelen kutusunda e-ticaret maili yok).
- Belirsiz kategorisindeki mailler doğası gereği tutarsız etiketli; bu kategorinin rakamlarını tek başına yorumlamayın.
- Yalnızca Windows; imzasız `.exe` (ilk açılışta SmartScreen uyarısı, kurulum yönergesinde anlatıldı). Doğrudan mail hesabına bağlanma (IMAP) yok, mailler dosya olarak verilir.
- Temiz bir bilgisayarda (Python'suz) gerçek deneme yapılmadı; yalnızca PATH temizlenerek simüle edildi.

## 6. Teklifte söylenebilecek / söylenemeyecek
- Söylenebilir: "Test setimizde maillerin yaklaşık %80'ini otomatik ayırdı, ayırdıklarının yaklaşık %85'i doğruydu; kalanı insana bıraktı. Sürekli düzeltmeyle iyileşir."
- Söylenemez: "%90 doğruluk", "gerçek maillerde ölçüldü", "hatasız".
- Öneri: İlk müşteriyle küçük bir pilot (birkaç yüz gerçek mail, müşterinin onayıyla): gerçek rakam o pilottan çıkar.

## 7. Teslim edilenler
`dist/MailSiniflandirma/` (Windows `.exe`, `python derle.py` ile üretilir), `teslimat/KURULUM.md`, `teslimat/ornek_rapor.xlsx`, `teslimat/ekran_goruntusu.png`.
