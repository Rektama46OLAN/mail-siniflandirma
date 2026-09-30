"""Mail Sınıflandırma masaüstü penceresi (Tkinter).  Çalıştırma: python uygulama.py

Klasör seç → Sınıflandır → sonuçları tabloda gör → Excel'e kaydet. Mailler yalnızca okunur, hiçbir dosya değiştirilmez.
"""
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from mailsinif import oku, rapor
from mailsinif.motor import Motor

RENK_ACIL, RENK_KONTROL = "#FCE4D6", "#FFF2CC"


class Uygulama(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mail Sınıflandırma")
        self.geometry("1100x640")
        self.minsize(900, 500)
        self.kuyruk: queue.Queue = queue.Queue()
        self.motor: Motor | None = None
        self.sonuclar: list[dict] = []
        self.okunamayan: list[str] = []
        self.calisiyor = False

        ust = ttk.Frame(self, padding=10)
        ust.pack(fill="x")
        ttk.Label(ust, text="Mail klasörü:").pack(side="left")
        self.klasor = tk.StringVar()
        ttk.Entry(ust, textvariable=self.klasor).pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(ust, text="Seç…", command=self.sec).pack(side="left")
        self.dugme = ttk.Button(ust, text="Sınıflandır", command=self.baslat)
        self.dugme.pack(side="left", padx=(10, 0))
        self.excel_dugme = ttk.Button(ust, text="Excel'e kaydet", command=self.kaydet, state="disabled")
        self.excel_dugme.pack(side="left", padx=(6, 0))

        self.ozet = tk.StringVar(value=".eml, .mbox veya .csv dosyalarının bulunduğu klasörü seçin.")
        ttk.Label(self, textvariable=self.ozet, padding=(10, 0)).pack(fill="x")
        self.bar = ttk.Progressbar(self, mode="determinate")
        self.bar.pack(fill="x", padx=10, pady=6)

        kolonlar = ("kaynak", "konu", "kategori", "guven", "acil", "kontrol")
        govde = ttk.Frame(self, padding=(10, 0, 10, 10))
        govde.pack(fill="both", expand=True)
        self.tablo = ttk.Treeview(govde, columns=kolonlar, show="headings")
        for k, b, w in (("kaynak", "Dosya", 170), ("konu", "Konu", 380), ("kategori", "Kategori", 150),
                        ("guven", "Güven", 70), ("acil", "Acil", 60), ("kontrol", "Kontrol", 90)):
            self.tablo.heading(k, text=b)
            self.tablo.column(k, width=w, anchor="w")
        self.tablo.tag_configure("acil", background=RENK_ACIL)
        self.tablo.tag_configure("kontrol", background=RENK_KONTROL)
        kay = ttk.Scrollbar(govde, orient="vertical", command=self.tablo.yview)
        self.tablo.configure(yscrollcommand=kay.set)
        self.tablo.pack(side="left", fill="both", expand=True)
        kay.pack(side="right", fill="y")
        self.after(100, self.kuyruk_isle)

    def sec(self):
        k = filedialog.askdirectory(title="Mail klasörünü seçin")
        if k:
            self.klasor.set(k)

    def baslat(self):
        if self.calisiyor:
            return
        if not self.klasor.get():
            messagebox.showinfo("Klasör seçin", "Önce mail dosyalarının bulunduğu klasörü seçin.")
            return
        self.calisiyor = True
        self.dugme.config(state="disabled")
        self.excel_dugme.config(state="disabled")
        self.tablo.delete(*self.tablo.get_children())
        self.bar.config(value=0)
        self.ozet.set("Çalışıyor…")
        threading.Thread(target=self.is_parcacigi, args=(self.klasor.get(),), daemon=True).start()

    def is_parcacigi(self, klasor):
        try:
            if self.motor is None:
                self.kuyruk.put(("mesaj", "Model hazırlanıyor (ilk çalıştırmada birkaç saniye sürer)…"))
                self.motor = Motor.yukle_veya_egit()
            self.kuyruk.put(("mesaj", "Mailler okunuyor…"))
            mailler, hatalar = oku.oku_klasor(klasor)
            sonuc = []
            for i, m in enumerate(mailler, 1):
                sonuc.append({**m, **self.motor.siniflandir(m["konu"], m["govde"])})
                if i % 5 == 0 or i == len(mailler):
                    self.kuyruk.put(("ilerleme", i, len(mailler)))
            self.kuyruk.put(("bitti", sonuc, hatalar))
        except Exception as e:
            self.kuyruk.put(("hata", str(e)))

    def kuyruk_isle(self):
        try:
            while True:
                o = self.kuyruk.get_nowait()
                if o[0] == "mesaj":
                    self.ozet.set(o[1])
                elif o[0] == "ilerleme":
                    self.bar.config(maximum=o[2], value=o[1])
                    self.ozet.set(f"Sınıflandırılıyor… {o[1]}/{o[2]}")
                elif o[0] == "bitti":
                    self.bitti(o[1], o[2])
                elif o[0] == "hata":
                    self.calisiyor = False
                    self.dugme.config(state="normal")
                    self.ozet.set("Hata oluştu.")
                    messagebox.showerror("Hata", o[1])
        except queue.Empty:
            pass
        self.after(100, self.kuyruk_isle)

    def bitti(self, sonuc, hatalar):
        self.calisiyor = False
        self.dugme.config(state="normal")
        self.sonuclar, self.okunamayan = sonuc, hatalar
        for s in sonuc:
            etiket = ("acil",) if s["acil"] else (("kontrol",) if s["kontrol"] else ())
            self.tablo.insert("", "end", tags=etiket, values=(
                s["kaynak"], s["konu"], s["kategori"], f"{s['guven']:.0%}", "ACİL" if s["acil"] else "",
                "kontrol et" if s["kontrol"] else ""))
        n = len(sonuc)
        bel = sum(s["kategori"] == "Belirsiz" for s in sonuc)
        metin = (f"{n} mail: {n - bel} sınıflandırıldı, {bel} Belirsiz, "
                 f"{sum(s['acil'] for s in sonuc)} acil, {sum(s['kontrol'] for s in sonuc)} kontrol listesinde.")
        if hatalar:
            metin += f" {len(hatalar)} dosya okunamadı."
        self.ozet.set(metin if n else "Klasörde okunabilir mail bulunamadı (.eml, .mbox, .csv).")
        self.excel_dugme.config(state="normal" if n else "disabled")

    def kaydet(self):
        yol = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")],
                                           initialfile="mail_siniflandirma_raporu.xlsx")
        if not yol:
            return
        try:
            rapor.yaz(self.sonuclar, yol, self.okunamayan)
            messagebox.showinfo("Kaydedildi", f"Rapor kaydedildi:\n{yol}")
        except PermissionError:
            messagebox.showerror("Kaydedilemedi", "Dosya başka bir programda açık olabilir. Kapatıp tekrar deneyin.")
        except Exception as e:
            messagebox.showerror("Kaydedilemedi", str(e))


if __name__ == "__main__":
    Uygulama().mainloop()
