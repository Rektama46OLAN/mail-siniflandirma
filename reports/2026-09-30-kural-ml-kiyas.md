# Faz 3: kural vs ML vs birleşik, 2026-09-30

Kod: `mailsinif/ml.py`, `olc_ml.py`. ML = TF-IDF (kelime 1-2 gram + karakter 2-5 gram) + lojistik regresyon.
Protokol: ML **dev'de eğitildi** (n=134); C=100 ve Belirsiz olasılık eşiği=0,3 yalnızca dev üzerinde
5-katlı çapraz doğrulamayla seçildi (Belirsiz ≤%17 kısıtıyla). Ölçüm **test'te** (n=141), kuralla aynı bölünme.
Birleşik = kural emin ise (Belirsiz değil ve güven ≥0,5) kural, değilse ML.

## Test kıyası

| Yöntem | Emin maillerde doğruluk | Genel doğruluk | Belirsiz oranı | Acil P/R |
|---|---|---|---|---|
| Kural (sürüm 2) | %76,9 | %70,9 | %17,0 | %76 / %92 |
| ML (134 mail ile eğitildi) | %71,2 | %65,2 | %16,3 | %76 / %92 |
| Birleşik | %77,2 | %74,5 | %9,9 | %76 / %92 |

Ek: tüm veri (275) üzerinde 5-katlı CV ×3 tohum, ML (her katta ~220 mail eğitim): emin doğruluk **%77,3 (±1,3)**, Belirsiz %13,0.

## Kategori bazında recall (test)

| Kategori | Kural | ML | Birleşik |
|---|---|---|---|
| Sipariş | %78 | %61 | %78 |
| Fatura | %83 | %44 | %78 |
| Şikayet | %17 | %33 | %39 |
| Soru | %78 | %61 | %89 |
| Belge | %100 | %100 | %100 |
| Otomatik | %94 | %94 | %94 |
| Spam | %50 | %72 | %67 |
| Belirsiz | %67 | %53 | %47 |

## Yorum
- **Hiçbiri belirgin iyi değil.** Kural ile birleşik arasındaki fark (%76,9 vs %77,2) n=141'de tesadüf sınırında
  (tek mail ≈ 0,7 puan, standart hata ≈ ±3,5 puan).
- **Hiçbiri %90 hedefine yakın değil.** En iyi rakamlar %77 civarı.
- ML küçük veriyle (134) kuraldan kötü; 220 mailin eğitimiyle (CV) kurala eşitleniyor. Öğrenme eğrisi hâlâ yükseliyor
  olabilir, ama bu bir tahmin: ölçülmedi.
- Kural ve ML farklı yerlerde güçlü: ML Spam ve Şikayet'te kuraldan iyi, Fatura/Sipariş'te kötü. Birleşik bu iki gücü
  toplayıp Belirsiz'i %9,9'a indiriyor, yani daha çok mail sınıflandırıyor (genel doğruluk %74,5 ile en iyi).
- Şikayet her yöntemde en zayıf kategori (%17-39 recall). Sorun yöntem değil, sinyalin dolaylı anlatımda olması.
- Gerçek dışı iyimserlik uyarısı: veri sentetik ve tek "yazar" tarafından üretildi; gerçek maillerde düşmesi beklenir.

## Öneri (Arda'nın kararı bekliyor)
Yöntem olarak **birleşik** seçilmesi: doğruluk eşit, kapsam daha geniş, iki yaklaşım birbirinin boşluğunu dolduruyor.
%90 hedefi için asıl kaldıraç yöntem değil **veri**: daha çok etiketli (özellikle Şikayet, Spam ve Belirsiz) ve
gerçek/temizlenmiş mail. Hedefi düşürmek ya da veri artırmak Arda'nın kararı.
