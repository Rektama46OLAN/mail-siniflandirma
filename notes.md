# Notlar — Mail Sınıflandırma

Çalışan tasarım dokümanı. Arda buraya fikirlerini atar, Rekt ile konuşulur,
olgunlaşınca Rekt aşağıya işler. Karar değişirse burası güncellenir.

Karara bağlanan ve artık tartışılmayan maddeler `const.md`'ye taşınır.

## Akış

1. Arda fikri paylaşır.
2. Rekt ile tartışılır / netleştirilir.
3. Onay verilince Rekt fikri aşağıya işler.
4. Karar kesinleşince `const.md`'ye gerekçesiyle geçer.

---

## Stack

| Katman | Seçim |
|---|---|
| Dil | Python |
| Sınıflandırma | Kural tabanlı baseline → TF-IDF + lojistik regresyon (scikit-learn), gerekirse ikisi birleşik |
| Mail girdisi | `.eml` / `.mbox` / CSV klasörü (bağlantısız) |
| Arayüz | Basit masaüstü penceresi (toolkit henüz seçilmedi — açık madde) |
| Rapor | Excel (.xlsx) |
| Test seti | ~300 yapay Türkçe e-ticaret maili, elle doğrulanmış etiket |

Kaynak: `2026-09-29-eposta-siniflandirma-karar-ozeti.md` (ArdaOS Inbox/Dump). Kararlar oradan alındı.

**Amaç:** Freelance AI otomasyon hizmetinin ana ürünü olan mail sınıflandırmanın kanıt projesi.
Doğruluk rakamı teklif aşamasının ana kanıtı. Kanıt bitmeden teklif yok.

**Kategoriler (8):** Sipariş/Talep, Fatura/Ödeme, Şikayet/Sorun, Soru/Bilgi, Belge/Evrak,
Otomatik bildirim, Reklam/Spam, Belirsiz. Ayrıca kategoriden bağımsız **Acil** işareti.

**Hedef:** emin olunan maillerde >%90 doğruluk; mailin en fazla %15-20'si "Belirsiz".

---

## Faz Planı

Her fazın **bitiş kriteri** yazılır — "bitti" ölçülebilir olsun diye.
Faz uzun görünüyorsa ikiye böl; ilerleme ölçülemeyen faz faz değildir.

| Faz | İçerik | Bitiş kriteri |
|---|---|---|
| **0** | Planlama iskeleti, git, GitHub | `kur.py --kontrol` temiz; repo public'te |
| **1a** | Test maili üretimi (subagent A, kategori başına 1, kişilik çeşitliliği) | 8 kategori × ~35 mail dosyada; her mailde konu/gövde/gönderen tipi/niyet edilen kategori/acil |
| **1b** | Bağımsız etiket denetimi (subagent B) + Arda incelemesi | Uyuşmayan liste çıkmış; Arda onayladıktan sonra `etiketli` set dondurulmuş |
| **2** | Kural tabanlı baseline + ölçüm betiği | Test setinde kategori doğruluğu, Belirsiz oranı, karışıklık matrisi `reports/`'ta |
| **3** | TF-IDF + lojistik regresyon, aynı sette kıyas (çapraz doğrulama) | Kural vs ML vs birleşik tablosu `reports/`'ta; seçim gerekçesi const.md'de |
| **4** | Masaüstü pencere + Excel rapor (kategori, güven, acil, yanlışları görme listesi) | Örnek klasör seçilip pencereden çalıştırılınca .xlsx üretiliyor |
| **4b** | Windows paketleme (PyInstaller onedir), yol düzeltmeleri, kurulum yönergesi | Python'suz ortamda `.exe` mail klasörünü okuyup Excel üretiyor; pencere açılıyor |
| **5** | Kanıt raporu, Excel düzeltme geri beslemesi, ArdaOS'a rapor | Hedef doğruluk ölçüldü; rapor `reports/`'ta; düzeltmeler pencereden yüklenip model yeniden eğitiliyor; ArdaOS'a rapor edildi (tamamlandı 2026-09-30) |

**Faz 1b Arda'ya bağlı:** etiket doğrulamasının son sözü Arda'da. Arda uzaktayken 1a ve
sonrası ilerleyebilir ama sonuçlar "onaysız etiket" ile üretilir; 1b onayı gelince yeniden ölçülür.

---

## Ölçüm protokolü (Faz 2-3)

- Dev = çift numaralı id (~137 mail), test = tek numaralı id (~138 mail). Kurallar/eşikler yalnızca dev hatalarına bakılarak ayarlanır; test'e ayar sırasında bakılmaz.
- İlk kural sürümü mailler okunmadan, alan bilgisiyle yazıldı; ayarsız ilk ölçüm `reports/`'ta "ilk atış" olarak saklanır.
- Raporlanan rakamlar: genel doğruluk (Belirsiz de sınıf), emin olunan maillerde doğruluk (tahmin≠Belirsiz), Belirsiz oranı, Acil precision/recall, kategori bazında recall/precision.
- Kod: `mailsinif/` (metin, kural, olcum), çalıştırma `python olc_kural.py [--hatalar dev]`.

---

## Fikirler

- Gerçek (temizlenmiş) birkaç mail test setine eklensin — sentetik veri kuralları olduğundan iyi gösterir.
- LLM opsiyonel katman: sadece düşük güvenli maillerde, müşteri onaylı, müşterinin kendi API anahtarıyla.
- Sektör "paketleri": e-ticaret için ileride iade/kargo takibi ayrı kategori olabilir.

---

## Açık maddeler

- **Doğruluk hedefi revizyonu (Arda karar verecek).** Birleşik yöntem seçildi (const.md). Doğruluk-kapsam eğrisi (`reports/2026-09-30-dogruluk-kapsam-egrisi.md`):
  >%90 doğruluk için Belirsiz ≈%40-45 gerekiyor; Belirsiz %15-20'de doğruluk ≈%83-85. Eski hedef çifti (>%90 ve ≤%15-20) sağlanamıyor.
  Seçenekler: (1) "%90 doğru, yarısı insana" (2) "%80'ini ayırır, %85 doğru" (3) sentetikte kalarak veri artışıyla eğriyi yukarı kaydırmak.
  Gerçek test seti kullanılmayacak (Arda: kendi maillerinde e-ticaret yok); rakamlar sentetik, teklifte bu açıkça söylenmeli.
- **Ürün özelliği:** Excel'deki "yanlışları görme listesi" müşteri düzeltmelerini toplayıp yeniden eğitimi besleyecek ("kullandıkça öğrenir"). Faz 4/5'e girer.

- GUI toolkit seçimi (Tkinter yerleşik ve bağımlılıksız — öneri; Arda onaylamadı).
- KVKK / veri işleme koşulları (opsiyonel LLM katmanı için) — değerlendirilmedi.
- Teklif metni, fiyatlandırma, hedef müşteri listesi — konuşulmadı.

---

## Rafta

Şimdilik yapılmayacak, ama unutulmasın diye duranlar.

- IMAP salt-okunur bağlantı (uygulama şifresi). Kanıt projesinin kapsamı dışı.
- Gmail/Outlook resmi API/OAuth.
- Yan hizmetler: belge/veri işleme, rapor üretme.
- Microsoft 365 kurumsal IMAP basit şifre kapalı olabilir — sahada netleşir.
