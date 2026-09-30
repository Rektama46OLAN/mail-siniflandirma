# Birleşik yöntem: doğruluk-kapsam eğrisi, 2026-09-30

Kod: `olc_egri.py`. Kapsam = Belirsiz'e düşmeyen mail oranı; doğruluk = kapsanan maillerdeki doğruluk.
Gerçekte Belirsiz olan mailler de veri setinde (test'te 15/141), sistem bunları Belirsiz'e ayıramazsa hata sayılır.
İki düğme taranıp Pareto sınırı alındı: kural güven eşiği ve ML olasılık eşiği.

**Uyarı:** Eşikler ölçüm verisi üzerinde tarandığı için rakamlar hafif iyimser. Üretimde eşik ayrı veriyle seçilmeli.
CV tablosu daha güvenilir (her katta ML yeniden eğitilir); kural dev'de ayarlanmış olduğundan yine de hafif iyimser.

## Tüm veri, 5-katlı CV ×3 tohum (n=275)

| Kapsam | Belirsiz | Doğruluk |
|---|---|---|
| %56 | %44 | %90,1 |
| %65 | %35 | %88,0 |
| %73 | %27 | %86,4 |
| %80 | %20 | %85,0 |
| %83 | %17 | %83,3 |
| %87 | %13 | %82,8 |
| %92 | %8 | %80,5 |
| %95 | %5 | %76,6 (eşiksiz) |

## Test seti (ML dev'de eğitildi, n=141)

| Kapsam | Belirsiz | Doğruluk |
|---|---|---|
| %47 | %53 | %92,4 |
| %57 | %43 | %91,4 |
| %62 | %38 | %88,5 |
| %73 | %27 | %87,4 |
| %78 | %22 | %85,5 |
| %82 | %18 | %80,9 |
| %90 | %10 | %77,2 |

## Yorum
- **%90 doğruluğa ulaşmak için maillerin yaklaşık %40-45'i Belirsiz'e bırakılmalı** (kapsam %55-57). Bu, hedefteki %15-20 Belirsiz ile çelişiyor.
- **Belirsiz %15-20 iken doğruluk ≈ %83-85** (CV). Yani mevcut hedef çifti (>%90 ve ≤%15-20) bu veri ve yöntemle birlikte sağlanamıyor.
- İki mantıklı sunum: "ayırdığının %90'ı doğru, yaklaşık yarısını insana bırakır" ya da "mailin %80'ini ayırır, ayırdığının %85'i doğru".
  İkisi de dürüst; hangisi müşteriye daha çok değer katar sorusu ürün kararı.
- Veri arttıkça bu eğri yukarı kayar (öğrenme eğrisi: 4× veri → +4 puan doğruluk, Belirsiz %34→%13), ama sentetik veriyle bir yere kadar.
