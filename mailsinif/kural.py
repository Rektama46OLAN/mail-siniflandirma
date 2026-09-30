"""Kural tabanlı sınıflandırıcı (baseline).

Her kategori için regex kalıpları (normalleştirilmiş, aksansız metinde) ve ağırlıkları var.
Konu satırındaki eşleşme ikiye katlanır. En yüksek puan kazanır; puan düşükse ya da
ikinciyle fark azsa "Belirsiz". Güven = fark tabanlı, 0-1.

Sürüm 2: dev hatalarına bakılarak ayarlandı (test'e bakılmadı). İlk atış: reports/2026-09-30-kural-ilk-atis.md
"""
import re

from .metin import normalle

KATEGORILER = [
    "Sipariş / Talep", "Fatura / Ödeme", "Şikayet / Sorun", "Soru / Bilgi",
    "Belge / Evrak", "Otomatik bildirim", "Reklam / Spam", "Belirsiz",
]

# (kalıp, ağırlık) — kalıplar normalleştirilmiş metne uygulanır
KURALLAR = {
    "Sipariş / Talep": [
        (r"siparis", 1), (r"iptal", 1.5), (r"adet", 1), (r"toplu", 1), (r"almak istiyorum", 1.5),
        (r"vermek istiyorum|verebilir miyim", 1.5), (r"ekleyebilir", 1), (r"adres degis", 1.5), (r"degistirmek", 1),
        (r"rezerve", 1.5), (r"ozel (?:uretim|talep|olcu)|yaptirmak", 1.5), (r"hediye paketi|not ekle", 1.5),
        (r"kargoya ver(?:ir|ebilir)", 1),
    ],
    "Fatura / Ödeme": [
        (r"fatura", 2), (r"odeme", 1.5), (r"dekont", 2), (r"havale|\beft\b", 1.5), (r"iban", 1.5),
        (r"taksit", 1.5), (r"tahsil", 1), (r"\bkdv\b", 1.5), (r"e-?arsiv|e-?fatura", 2),
        (r"kart(?:tan|im\w*|ima)? \w*\s?(?:para )?cek", 2), (r"para(?:m|si|nin)? (?:iade|cek|yat|gel)", 2),
        (r"iade tutari|ucret iade|iade paras", 2), (r"vergi no", 1), (r"hakedis|yatan tutar|hesabima yat", 2),
        (r"iki kez cek|cift cek|blokede", 2), (r"cuzdan", 1),
    ],
    "Şikayet / Sorun": [
        (r"sikayet", 2), (r"memnun degil|memnun kalmadim|memnuniyetsiz", 2), (r"hasarli|kirik|kirilmis|yirtik|lekeli", 2),
        (r"bozuk|calismiyor|arizali|arizalan", 2), (r"(?:yanlis|farkli|eksik|ezik|ezil|hasar|kirik|bozuk)\w* (?:gel|gon)", 2.5),
        (r"gelmedi|ulasmadi|hala gelmedi|hala yok", 1.5), (r"gecik", 1.5), (r"rezalet|berbat|kabul edilemez|skandal|sacma", 2),
        (r"iade edic|iade ede|iade etmek|degisim", 1.5), (r"magdur|hayal kirikligi|tepki|sitem", 1.5), (r"kayip", 1),
        (r"kimse (?:donmuyor|cevap)|donus yapilmiyor|ulasamiyorum", 2), (r"ucuncu kez|tekrar tekrar|yine ayni", 2),
        (r"kargoya bile verilmemis|hala hazirlaniyor", 2),
    ],
    "Soru / Bilgi": [
        (r"stok", 1), (r"\bbeden\b", 1), (r"kac gun", 1.5), (r"var mi|mevcut mu|bulunur mu|satista mi", 1.5),
        (r"bilgi (?:almak|verir|rica)", 1.5), (r"nasil (?:yapilir|kullan|calis)", 1), (r"uyumlu mu|uyar mi", 1.5),
        (r"calisma saat", 1.5), (r"iade (?:sartlari|politika|kosul)", 1.5), (r"fiyat", 1), (r"kargo (?:ucreti|suresi|firmasi)", 1),
        (r"\?", 0.5), (r"merak ediyorum|ogrenmek istiyorum|ogrenebilir", 1.5), (r"mumkun mu|olur mu|misiniz|musunuz", 1),
        (r"sorum var|bir sey soracagim|hakkinda bilgi|yurt disi", 1.5), (r"henuz siparis vermedim|dusunuyorum|bakiyorum", 2),
        (r"kac sayfa|hangi yas|ne kadar dayan|yikamada", 1.5),
    ],
    "Belge / Evrak": [
        (r"\bekte\b|\bekteki|\bekli\b|\bektedir", 2), (r"\[ek:", 5), (r"\.(?:pdf|docx?|xlsx?|jpg|png)\b", 2),
        (r"imzali|imzalay|kase", 1.5), (r"sozlesme", 2), (r"vergi levha", 2), (r"irsaliye", 2),
        (r"\bform\b|formu", 1.5), (r"proforma", 2), (r"\bteklif", 1), (r"katalog", 1.5), (r"belge|evrak", 1.5),
    ],
    "Otomatik bildirim": [
        (r"no-?reply|do not reply", 3), (r"bu (?:e-?posta|mail)(?:e|i)? (?:otomatik|yanitlamayin|cevaplamayin)", 3),
        (r"otomatik (?:olarak|bildirim|yanit|mesaj)|auto-?reply", 2.5), (r"yanit vermeyin|cevap vermeyin|yanitlamayin", 3),
        (r"takip ?(?:no|numarasi|kodu|:)|\bdurum:", 2), (r"kargoya verildi|dagitima cikti|teslim edildi|sube(?:mize)? ulasti|aktarma merkez", 2),
        (r"dogrulama kodu|sifre(?:nizi)? sifirla|giris denemesi|guvenlik uyarisi", 2.5),
        (r"yeni siparis|siparis ozeti", 1.5), (r"bildirim|uyarisi", 1.5), (r"tatildeyim|ofis(?:imiz)? (?:disinda|kapali)|out of office", 3),
        (r"panel|dashboard|raporunuz", 1), (r"\|", 2), (r"sayin (?:uye|musterimiz|kullanici|iyeri)", 1.5),
        (r"aktarilmistir|olusturulmustur|kesilmistir|gonderilmistir|tanimlanmistir", 2.5), (r"teessuf|rica olunur", 0.5),
    ],
    "Reklam / Spam": [
        (r"kampanya|indirim|firsat", 1), (r"tikla|hxxp|\[\.\]", 2.5), (r"kazandiniz|cekilis", 2.5), (r"hediye", 0.5),
        (r"\bseo\b|reklam ajans|sosyal medya yonetim", 2.5), (r"abone|bulten|abonelikten", 2), (r"kredi|kripto|yatirim", 2),
        (r"askiya (?:alin|al)|hesabiniz.*(?:kapat|askiya)|dogrulayin|kimlik bilgi", 2.5), (r"son \d+ saat|kacirmayin|sinirli sure", 2),
        (r"isbirligi|is birligi|ortaklik", 1.5), (r"toplu (?:kargo|paket)|paketleme|koli|dropshipping|stoksuz", 2),
        (r"!{2,}", 0.5), (r"size ozel|ozel teklif", 1.5),
        (r"satici(?:lara|larina|lar icin)|e-ticaret (?:firmalari|magaza)|magaza ekibi|magazaniz(?:in)? icin", 2.5),
        (r"sunuyoruz|sunmaktayiz|olarak .{0,40}hizmet|yorum paket|5 yildiz", 2),
        (r"tanisin|ucretsiz (?:deneme|demo)|indirimli", 1.5),
    ],
}

ACIL_KALIP = re.compile(
    r"\bbugun\b|\bhemen\b|\bacil\b|acilen|son gun|yarina|\ben gec\b|24 saat|derhal|bu aksam|bu hafta icinde|"
    r"vakit yok|gecikmeden|ivedi"
)

ESIK_MIN_PUAN = 1.5   # dev ölçümüyle ayarlanır
ESIK_FARK = 0.5


def puanla(konu: str, govde: str) -> dict:
    k, g = normalle(konu), normalle(govde)
    p = {}
    for kat, kurallar in KURALLAR.items():
        s = 0.0
        for kalip, w in kurallar:
            if re.search(kalip, k):
                s += 2 * w
            if re.search(kalip, g):
                s += w
        p[kat] = s
    return p


def acil_mi(konu: str, govde: str) -> bool:
    return bool(ACIL_KALIP.search(normalle(konu + " " + govde)))


def siniflandir(konu: str, govde: str) -> dict:
    p = puanla(konu, govde)
    sirali = sorted(p.items(), key=lambda t: -t[1])
    (ilk, s1), (_, s2) = sirali[0], sirali[1]
    fark = s1 - s2
    kat = ilk if (s1 >= ESIK_MIN_PUAN and fark >= ESIK_FARK) else "Belirsiz"
    guven = 0.0 if s1 <= 0 else min(1.0, fark / max(s1, 1e-9))
    return {"kategori": kat, "guven": round(guven, 3), "acil": acil_mi(konu, govde), "puanlar": p}
