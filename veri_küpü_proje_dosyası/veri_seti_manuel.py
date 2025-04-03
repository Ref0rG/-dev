import os
import csv
import tkinter as tk
from tkinter import messagebox

dosya_adi = ""
sutunlar = []
veri_kutulari = {}

def veri_seti_adi_al():
    global dosya_adi
    dosya_adi = veri_seti_giris.get().strip()
    
    if not dosya_adi:
        messagebox.showwarning("Uyarı", "Lütfen veri seti adını girin!")
        return
    
    veri_seti_giris.config(state=tk.DISABLED)
    veri_seti_onay_butonu.config(state=tk.DISABLED)

    sutun_sayisi_cerceve.grid(row=3, column=0, columnspan=2, pady=10)

def sutun_sayisi_al():
    try:
        sutun_sayisi = int(sutun_sayisi_giris.get().strip())
        if sutun_sayisi <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Uyarı", "Lütfen geçerli bir sütun sayısı girin!")
        return
    
    sutun_sayisi_giris.config(state=tk.DISABLED)
    sutun_sayisi_onay_butonu.config(state=tk.DISABLED)
    
    sutunlari_al(sutun_sayisi)

def sutunlari_al(sutun_sayisi):
    global sutunlar, veri_kutulari
    
    sutunlar.clear()
    veri_kutulari.clear()
    
    sutun_sayisi_cerceve.grid_forget()  # Sütun sayısı giriş alanını gizle

    for i in range(sutun_sayisi):
        label = tk.Label(sutun_cercevesi, text=f"Sütun {i+1} Adı:")
        label.grid(row=i, column=0, padx=5, pady=2, sticky="w")
        
        sutun_giris = tk.Entry(sutun_cercevesi)
        sutun_giris.grid(row=i, column=1, padx=5, pady=2)
        
        veri_kutulari[f"sutun_{i+1}"] = sutun_giris
    
    sutunlari_onayla_buton.grid(row=sutun_sayisi, column=0, columnspan=2, pady=10)
    sutun_cercevesi.grid(row=4, column=0, columnspan=2, pady=10)

def sutunlari_onayla():
    global sutunlar
    
    for key in veri_kutulari:
        sutun_adi = veri_kutulari[key].get().strip()
        if not sutun_adi:
            messagebox.showwarning("Uyarı", "Sütun adı boş bırakılamaz!")
            return
        sutunlar.append(sutun_adi)
    
    sutun_cercevesi.grid_forget()         # Sütun isimleri giriş alanlarını gizle
    sutunlari_onayla_buton.grid_forget()   # Butonu gizle

    veri_giris_arayuzu_olustur()

def veri_giris_arayuzu_olustur():
    for i, sutun in enumerate(sutunlar):
        tk.Label(veri_cercevesi, text=sutun, font=('Arial', 10, 'bold')).grid(row=i, column=0, padx=5, pady=5, sticky="w")
        
        giris_kutusu = tk.Entry(veri_cercevesi)
        giris_kutusu.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
        
        veri_kutulari[sutun] = giris_kutusu
    
    kaydet_buton.grid(row=len(sutunlar), column=0, columnspan=2, pady=10)
    veri_cercevesi.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

def veriyi_kaydet():
    if not dosya_adi or not sutunlar:
        messagebox.showwarning("Uyarı", "Lütfen önce veri seti adını girin ve sütunları belirleyin!")
        return
    
    yeni_kayit = {sutun: veri_kutulari[sutun].get().strip() for sutun in sutunlar}
    
    klasor_yolu = "veri_setleri"
    if not os.path.exists(klasor_yolu):
        os.makedirs(klasor_yolu)
    dosya_yolu = os.path.join(klasor_yolu, f"{dosya_adi}.csv")
    
    dosya_var = os.path.exists(dosya_yolu)
    
    with open(dosya_yolu, mode='a', newline='', encoding='utf-8') as dosya:
        yazici = csv.DictWriter(dosya, fieldnames=sutunlar)
        if not dosya_var:
            yazici.writeheader()
        yazici.writerow(yeni_kayit)
    
    messagebox.showinfo("Başarılı", "Veri başarıyla kaydedildi!")
    
    for sutun in veri_kutulari:
        veri_kutulari[sutun].delete(0, tk.END)

# Ana pencere oluşturma
pencere = tk.Tk()
pencere.title("Veri Seti Oluşturucu")
pencere.geometry("1000x550")

# Ana çerçeve
ana_cerceve = tk.Frame(pencere)
ana_cerceve.grid(row=0, column=0, padx=10, pady=10)

# Bilgilendirme etiketi (en üstte, diğer tüm girişlerin üstünde)
bilgi_metni = tk.Label(ana_cerceve, text="Oluşturacağınız bu veri setinde her kayıt için kaydet butonuna bastıktan sonra tekrar yeni gözlemlerinizi girerek işleminize devam edebilirsiniz.", 
                        fg="blue", font=("Arial", 10, "italic"), wraplength=900, justify="center")
bilgi_metni.grid(row=0, column=0, columnspan=2, pady=(0,10))

# Veri seti adı giriş alanı (Bilgilendirme metninin hemen altında, 10px boşluk ile)
veri_seti_cerceve = tk.Frame(ana_cerceve)
veri_seti_cerceve.grid(row=1, column=0, columnspan=2, pady=(0,10))

tk.Label(veri_seti_cerceve, text="Veri Seti Adı:").grid(row=0, column=0, padx=5)
veri_seti_giris = tk.Entry(veri_seti_cerceve, width=30)
veri_seti_giris.grid(row=0, column=1, padx=5)
veri_seti_onay_butonu = tk.Button(veri_seti_cerceve, text="Onayla", command=veri_seti_adi_al)
veri_seti_onay_butonu.grid(row=0, column=2, padx=5)

# Sütun sayısı giriş alanı (Başlangıçta gizli)
sutun_sayisi_cerceve = tk.Frame(ana_cerceve)
tk.Label(sutun_sayisi_cerceve, text="Sütun Sayısı:").grid(row=0, column=0, padx=5)
sutun_sayisi_giris = tk.Entry(sutun_sayisi_cerceve, width=10)
sutun_sayisi_giris.grid(row=0, column=1, padx=5)
sutun_sayisi_onay_butonu = tk.Button(sutun_sayisi_cerceve, text="Tamam", command=sutun_sayisi_al)
sutun_sayisi_onay_butonu.grid(row=0, column=2, padx=5)

# Sütun isimleri giriş alanı (Başlangıçta gizli)
sutun_cercevesi = tk.Frame(ana_cerceve)

# Sütunları onayla butonu (Başlangıçta gizli)
sutunlari_onayla_buton = tk.Button(ana_cerceve, text="Sütunları Onayla", command=sutunlari_onayla)

# Veri giriş alanı (Başlangıçta gizli)
veri_cercevesi = tk.Frame(ana_cerceve)

# Kayıt butonu (Veri giriş alanı içerisinde son satırda)
kaydet_buton = tk.Button(ana_cerceve, text="Verileri Kaydet", command=veriyi_kaydet)

# Ana döngüyü başlat
pencere.mainloop()
