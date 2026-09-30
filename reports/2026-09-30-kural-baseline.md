# Kural tabanlı baseline (sürüm 2): ölçüm, 2026-09-30

Dev = çift id (n=134), test = tek id (n=141). Kurallar yalnızca dev hatalarına bakılarak ayarlandı;
test hatalarına bakılmadı (test toplam rakamı her çalıştırmada görüldü, hata listesi görülmedi).
Hedef: emin maillerde >%90, Belirsiz ≤%15-20.

| Ölçü | İlk atış dev / test | Sürüm 2 dev | Sürüm 2 **test** |
|---|---|---|---|
| Genel doğruluk (Belirsiz de sınıf) | %59,7 / %63,8 | %78,4 | **%70,9** |
| Emin olunan maillerde doğruluk | %61,5 / %68,6 | %81,7 | **%76,9** |
| Belirsiz'e düşen oran | %12,7 / %16,3 | %10,4 | **%17,0** |
| Acil precision / recall | %81/%100 / %76/%92 | %81 / %100 | **%76 / %92** |

Dürüst rakam test sütunudur: dev'e ayar yapıldığı için dev şişkin (dev-test farkı ≈5 puan).

## Test'te kategori bazında (recall / precision)
Sipariş %78/%82, Fatura %83/%68, Şikayet **%17**/%60, Soru %78/%64, Belge %100/%82,
Otomatik %94/%89, Spam %50/%90, Belirsiz %67/%42.

## Karışıklık matrisi, test (satır = gerçek, sütun = tahmin)

| gerçek \ tahmin | Sipariş | Fatura | Şikayet | Soru | Belge | Otomatik | Reklam | Belirsiz |
|---|---|---|---|---|---|---|---|---|
| Sipariş | 14 | 2 | 0 | 1 | 0 | 0 | 0 | 1 |
| Fatura | 1 | 15 | 0 | 0 | 1 | 0 | 0 | 1 |
| Şikayet | 1 | 1 | 3 | 4 | 0 | 1 | 1 | 7 |
| Soru | 0 | 1 | 0 | 14 | 1 | 0 | 0 | 2 |
| Belge | 0 | 0 | 0 | 0 | 18 | 0 | 0 | 0 |
| Otomatik | 0 | 1 | 0 | 0 | 0 | 17 | 0 | 0 |
| Reklam | 0 | 2 | 1 | 0 | 2 | 1 | 9 | 3 |
| Belirsiz | 1 | 0 | 1 | 3 | 0 | 0 | 0 | 10 |

## Yorum
- Kural tabanlı yaklaşım hedefin (%90) altında kaldı: test'te emin maillerde %76,9.
- En zayıf halka **Şikayet**: 18 şikayet mailinin 7'si Belirsiz'e, 4'ü Soru'ya düşüyor. Şikayetler sabit kelimeyle değil,
  dolaylı anlatımla ("paket ezilmiş geldi", "bu üçüncü kez yazıyorum") geliyor; kalıp listesi bunu yakalayamıyor.
- **Spam** recall %50: meşru satıcıya yazılmış soğuk satış metinleri sıradan iş yazışmasına benziyor.
- Bundan sonra kural ayarlamak dev'e daha fazla uyum, test'e az kazanç getirir. Sıradaki adım Faz 3: aynı bölünmede
  TF-IDF + lojistik regresyon; kural ile ML aynı tabloda kıyaslanır.
- Uyarı: veri sentetik; gerçek maille rakamlar düşebilir.
