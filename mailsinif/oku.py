"""Mail dosyalarını okur: .eml, .mbox, .csv (kolonlar: konu, govde; isteğe bağlı gonderen). Salt okunur."""
import csv
import email
import html
import mailbox
import re
from email import policy
from pathlib import Path


def _duz(metin: str) -> str:
    metin = re.sub(r"(?is)<(script|style).*?</\1>", " ", metin)
    metin = re.sub(r"(?s)<[^>]+>", " ", metin)
    return re.sub(r"[ \t]+", " ", html.unescape(metin)).strip()


def _govde(msg) -> str:
    parca = msg.get_body(preferencelist=("plain", "html"))
    if parca is None:
        return ""
    try:
        icerik = parca.get_content()
    except Exception:  # bozuk charset
        icerik = (parca.get_payload(decode=True) or b"").decode("utf-8", "replace")
    return _duz(icerik) if parca.get_content_type() == "text/html" else icerik.strip()


def _mail(msg, kaynak: str) -> dict:
    return {"kaynak": kaynak, "gonderen": str(msg.get("From", "")), "konu": str(msg.get("Subject", "")),
            "govde": _govde(msg)}


def oku_klasor(klasor: str, ilerleme=None) -> tuple[list[dict], list[str]]:
    """Klasördeki (alt klasörler dahil) tüm mailleri okur. Döner: (mailler, okunamayanlar)."""
    mailler, hatalar = [], []
    dosyalar = sorted(p for p in Path(klasor).rglob("*") if p.suffix.lower() in (".eml", ".mbox", ".csv"))
    for i, p in enumerate(dosyalar):
        try:
            if p.suffix.lower() == ".eml":
                with open(p, "rb") as f:
                    mailler.append(_mail(email.message_from_binary_file(f, policy=policy.default), p.name))
            elif p.suffix.lower() == ".mbox":
                for j, m in enumerate(mailbox.mbox(str(p), factory=lambda f: email.message_from_binary_file(f, policy=policy.default)), 1):
                    mailler.append(_mail(m, f"{p.name}#{j}"))
            else:
                with open(p, encoding="utf-8-sig", newline="") as f:
                    for j, r in enumerate(csv.DictReader(f), 1):
                        r = {(k or "").strip().lower(): v for k, v in r.items()}
                        mailler.append({"kaynak": f"{p.name}#{j}", "gonderen": r.get("gonderen", ""),
                                        "konu": r.get("konu", ""), "govde": r.get("govde", "")})
        except Exception as e:
            hatalar.append(f"{p.name}: {e}")
        if ilerleme:
            ilerleme(i + 1, len(dosyalar))
    return mailler, hatalar
