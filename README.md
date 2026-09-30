# Mail Sınıflandırma

E-ticaret satıcılarının gelen e-postalarını kategoriye ayıran, **API'siz ve bağlantısız** çalışan Python aracı.
Bir klasördeki `.eml` / `.mbox` / `.csv` mail dosyalarını okur; her mail için kategori, güven skoru ve Acil işareti üretir;
sonucu masaüstü penceresinde gösterir ve Excel'e yazar. Mailler yalnızca okunur, hiçbir dosya değiştirilmez.

**Kategoriler:** Sipariş / Talep, Fatura / Ödeme, Şikayet / Sorun, Soru / Bilgi, Belge / Evrak, Otomatik bildirim,
Reklam / Spam, Belirsiz (emin değilse insana bırakılır). Acil, kategoriden bağımsız bir işarettir.

## Çalıştırma

```
pip install -r requirements.txt
python uygulama.py
```

Pencerede klasörü seçin (deneme için `ornek_mailler/`), **Sınıflandır**'a basın, sonra **Excel'e kaydet**.
Excel'de `Kontrol listesi` sayfası emin olunmayan mailleri toplar; "Doğru kategori" sütunu açılır liste ile doldurulur.

## Yöntem

Birleşik: önce kural tabanlı sınıflandırıcı (emin ise), değilse TF-IDF + lojistik regresyon.
Çalışma noktası: maillerin ~%80'i sınıflandırılır, sınıflandırılanların ~%85'i doğrudur.

**Bu rakamlar sentetik (yapay) Türkçe e-ticaret mailleriyle ölçüldü; gerçek maillerde farklı çıkabilir.**
Ölçüm raporları `reports/` altında. Test: `python test_akis.py`.
