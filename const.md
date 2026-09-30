# Sabitler (const)

Projedeki değişmez gerçekler burada tutulur. Bir şey buraya yazıldıysa verili kabul edilir;
değiştirmeden önce Arda'ya sorulur.

`notes.md` ile farkı: burası **karara bağlanmış ve artık tartışılmayan** maddeleri tutar.
`notes.md` çalışan tasarım dokümanıdır — detay, faz planı ve henüz açık maddeler oradadır.

## Yazım kuralı

Her madde: **kalın tek cümlelik karar** + altına `Gerekçe:`.
Gerekçe teoriden değil, yaşanandan yazılır — hangi sorunla karşılaşıldı, ne ölçüldü,
alternatifi neden düşürüldü. Gerekçesiz madde bir süre sonra "acaba neden böyleydi"
diye tekrar tartışılır; asıl maliyet orada.

---

## Gerçekler

### Kapsam

- **İlk hedef sektör e-ticaret satıcılarıdır; ilk sürüm sadece çekirdek 8 kategoriyi kapsar.**
  Gerekçe: Arda ve Rekt'in 2026-09-29 tartışmasında seçildi; yazılı ulaşım rahat, yüz yüze satış istenmiyor. Sektör uyarlaması sonra "paket" olarak eklenir.
- **Kategoriler: Sipariş/Talep, Fatura/Ödeme, Şikayet/Sorun, Soru/Bilgi, Belge/Evrak, Otomatik bildirim, Reklam/Spam, Belirsiz. Acil kategori değil, ayrı bir özelliktir.**
  Gerekçe: Liste Arda tarafından "tam" diye onaylandı. "Belirsiz" zorla tahmin yerine emin olunmayan maili insana bırakır; doğruluk "ayırdığının %X'i doğru" diye sunulabilir.
- **Doğruluk hedefi: emin olunan maillerde %90 üstü; mailin en fazla %15-20'si Belirsiz.**
  Gerekçe: Arda 2026-09-29'da onayladı.
- **Kanıt projesi bağlantısız çalışır; mail dosyalarını (.eml/.mbox/CSV) okur, IMAP yok.**
  Gerekçe: Teklif aşamasında ana kanıt elle etiketlenmiş test setindeki doğruluk rakamıdır. Sıra: kanıt projesi → teklifler.
- **Gerçek müşteri maili kullanılmaz; kendi gelen kutusundan alınacaksa kişisel bilgiler temizlenir.**
  Gerekçe: Veri saklama/gizlilik sorumluluğu alınmıyor (KVKK).

### Stack

- **Saf Python, API'siz; kural tabanlı + yerel ML (TF-IDF + lojistik regresyon).**
  Gerekçe: Müşteri verisi dışarı çıkmasın; maliyet sıfır. LLM yalnızca opsiyonel katman (düşük güvenli, müşteri onaylı, mümkünse müşterinin kendi API anahtarı).
- **ML zorunlu değil: önce kural tabanlı baseline, sonra aynı sette ML kıyası; belirgin iyi olan seçilir, gerekirse önce kural sonra ML.**
  Gerekçe: Test setini biz yazdığımız için kurallar sentetik veride iyi görünür; kıyas olmadan seçim kanıtsız olur. Kural "Belirsiz"i kaba (eşleşme sayısı) verir, ML olasılık verdiği için eşik ayarı kolaydır.
- **Sınıflandırma yöntemi birleşiktir: önce kural (emin ise), emin değilse ML (TF-IDF + lojistik regresyon, olasılık eşiğiyle Belirsiz).**
  Gerekçe: 2026-09-30 kıyasında (test, n=141) emin doğruluk kural %76,9, ML %71,2, birleşik %77,2; fark gürültü sınırında ama birleşik Belirsiz'i %17'den %9,9'a indirip daha çok mail sınıflandırıyor (genel doğruluk %74,5 ile en iyi). Kural ve ML farklı kategorilerde güçlü (ML Spam/Şikayet, kural Fatura/Sipariş). Arda 2026-09-30'da onayladı. Rapor: reports/2026-09-30-kural-ml-kiyas.md.
- **Çalışma noktası: maillerin ~%80'i sınıflandırılır (Belirsiz ~%20), sınıflandırılanların ~%85'i doğrudur. Varsayılan eşikler: kural güveni 0,5, ML olasılığı 0,5.**
  Gerekçe: Doğruluk-kapsam eğrisi (CV, n=275): %90 doğruluk maillerin ~%45'ini Belirsiz'e bırakmayı gerektiriyor; %20 Belirsiz'de %85. Arda 2026-09-30'da "%80'ini ayırır, ayırdığının %85'i doğru" senaryosunu seçti: e-ticaret satıcısı için asıl değer zaman kazanmak. Rakamlar sentetik veriye dayanır, teklifte bu açıkça söylenir. Eski hedef (>%90 ve ≤%15-20 Belirsiz) yerine geçer. Rapor: reports/2026-09-30-dogruluk-kapsam-egrisi.md.
- **Arayüz Tkinter ile yazılmış basit masaüstü penceresi, rapor Excel (openpyxl).**
  Gerekçe: Müşteri komut satırı değil düzgün bir şey görmeli; e-ticaret satıcıları Excel'e alışık. Tkinter Python'da yerleşik, müşteri bilgisayarına ek arayüz bağımlılığı kurulmaz (Arda 2026-09-30'da onayladı; PySide/PyQt daha modern ama kurulumu ağır).

### Mimari

- **Çalışma yeri müşterinin/Arda'nın kendi bilgisayarıdır; buluta yüklenen servis değil.**
  Gerekçe: Veri saklama sorumluluğu alınmıyor.
- **Mail bağlantısı (ileride): IMAP salt okunur, uygulama şifresiyle; silme/taşıma/cevaplama yok.**
  Gerekçe: En düşük riskli başlangıç. Resmi API/OAuth sonraki aşama. Şu an kapsam dışı.
- **Sınıflandırıcı, masaüstü penceresi ve Excel raporu kodu tek ana agent tarafından yazılır.**
  Gerekçe: Birbirine sıkı bağlı, bölünmez; her subagent sıfırdan başladığı için bağlam yükü kazancı geçer.

### Geliştirme

- **Subagent yalnızca iki iş için kullanılır: (A) kategori başına test maili üretimi, (B) yazarın etiketini görmeden bağımsız etiket denetimi.**
  Gerekçe: Kategori başına ayrı agent + farklı kişilikler tek agent'ın 300 maili aynı kalıba sokmasını önler. B, Arda'nın doğrulamasını hafifletir ama yerine geçmez; uyuşmayanlara Arda bakar, son söz onda.
- **Test setinde etiket doğrulamasının son sözü Arda'dadır.**
  Gerekçe: Etiketler yanlışsa doğruluk ölçümü anlamsızlaşır.
- **Ana agent ve subagentlar Sonnet ile başlar; zorlukta (kıyas yorumu, mimari karar, tıkanma) Opus'a yükseltilir.**
  Gerekçe: Darboğaz model gücü değil, etiket kalitesi ve sentetik verinin gerçekçiliği.
- **Test seti ~300 mail (kategori başına ~30-40), yapay Türkçe e-ticaret dili; yazım hataları, kısa/dağınık yazım katılır.**
  Gerekçe: Kanıt rakamı bu sete dayanır.
