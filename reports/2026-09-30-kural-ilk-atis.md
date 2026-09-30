# Kural tabanlı baseline: ilk atış (ayarsız), 2026-09-30

Kalıplar mailler okunmadan, alan bilgisiyle yazıldı; hiçbir ayar yapılmadı.
Dev = çift id (n=134), test = tek id (n=141). Hedef: emin maillerde >%90, Belirsiz ≤%15-20.

| Ölçü | Dev | Test |
|---|---|---|
| Genel doğruluk (Belirsiz de sınıf) | %59,7 | %63,8 |
| Emin olunan maillerde doğruluk | %61,5 | %68,6 |
| Belirsiz'e düşen oran | %12,7 | %16,3 |
| Acil precision / recall | %81 / %100 | %76 / %92 |

Kategori bazında recall (dev / test): Sipariş 47/78, Fatura 76/78, Şikayet 29/11, Soru 47/61,
Belge 94/100, Otomatik 65/67, Spam 65/56, Belirsiz 53/60.

Yorum: hedefin (%90) çok altında. En zayıf kategori Şikayet (test recall %11): şikayet mailleri çoğunlukla
sipariş/kargo sözcükleri içeriyor ve Sipariş'e kayıyor. Sonraki adım dev hatalarına bakıp kuralları ayarlamak.
