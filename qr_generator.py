import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import qrcode
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import sys


def get_base_path():
    """ Ottiene il percorso della cartella principale, sia in esecuzione da script che da .exe """
    if getattr(sys, 'frozen', False):  # Se l'eseguibile è congelato con PyInstaller
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def create_directories():
    """ Crea la cartella per il salvataggio se non esiste """
    base_path = get_base_path()
    qr_path = os.path.join(base_path, "qrcode")

    if not os.path.exists(qr_path):
        os.makedirs(qr_path)

    return qr_path


def generate_qr_code():
    """ Genera il QR Code e lo salva nella posizione scelta dall'utente """
    url = entry_url.get()
    qr_name = entry_name.get()
    save_path = entry_save_path.get()
    logo_file = entry_logo_path.get()

    if not url:
        messagebox.showerror("Errore", "Inserisci un URL valido!")
        return

    if not qr_name:
        qr_name = "qrcode"

    if not save_path:
        save_path = create_directories()

    qr_filename = os.path.join(save_path, f"{qr_name}.png")

    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=5,
    )
    qr.add_data(url)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

    if logo_file:
        qr_img = add_logo_to_qr(qr_img, logo_file, "white")

    qr_img.save(qr_filename)

    img = qr_img.resize((250, 250), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)

    label_qr.config(image=img)
    label_qr.image = img

    messagebox.showinfo("Successo", f"QR Code salvato in: {qr_filename}")


def add_logo_to_qr(qr_img, logo_path, color):
    """ Aggiunge un logo al centro del QR Code """
    logo = Image.open(logo_path)
    qr_width, qr_height = qr_img.size
    logo_size = int(qr_width * 0.3)
    logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    logo_bg_size = int(logo_size * 1.1)
    logo_bg = Image.new("RGBA", (logo_bg_size, logo_bg_size), color)
    logo_bg.paste(logo, ((logo_bg_size - logo_size) // 2, (logo_bg_size - logo_size) // 2), logo)

    pos = ((qr_width - logo_bg_size) // 2, (qr_height - logo_bg_size) // 2)
    qr_img.paste(logo_bg, pos, logo_bg)

    return qr_img

def choose_save_path():
    """ Permette all'utente di scegliere dove salvare il QR Code """
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_save_path.delete(0, tk.END)
        entry_save_path.insert(0, folder_selected)


def choose_logo():
    """ Permette all'utente di scegliere un logo per il QR Code """
    file_selected = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_selected:
        entry_logo_path.delete(0, tk.END)
        entry_logo_path.insert(0, file_selected)


# Creazione della finestra Tkinter con ttkbootstrap
root = ttk.Window(themename="cosmo")  # Tema moderno
root.title("Generatore QR Code - Made by Poppity")
root.geometry("650x750")
root.resizable(False, False)

# Titolo
label_title = ttk.Label(root, text="QR Code Generator", font=("Helvetica", 20, "bold"), bootstyle=PRIMARY)
label_title.pack(pady=10)

# Frame per l'input dell'URL
frame_input = ttk.Frame(root)
frame_input.pack(pady=5)

ttk.Label(frame_input, text="Inserisci l'URL:", font=("Helvetica", 12)).pack(anchor="w")
entry_url = ttk.Entry(frame_input, width=50, font=("Helvetica", 12), bootstyle="dark")
entry_url.pack(pady=3)

# Frame per il nome del QR Code
frame_name = ttk.Frame(root)
frame_name.pack(pady=5)

ttk.Label(frame_name, text="Nome del QR Code:", font=("Helvetica", 12)).pack(anchor="w")
entry_name = ttk.Entry(frame_name, width=30, font=("Helvetica", 12), bootstyle="dark")
entry_name.pack(pady=3)

# Frame per la scelta della cartella di salvataggio
frame_save = ttk.Frame(root)
frame_save.pack(pady=5)

ttk.Label(frame_save, text="Percorso di salvataggio:", font=("Helvetica", 12)).pack(anchor="w")
entry_save_path = ttk.Entry(frame_save, width=40, font=("Helvetica", 12), bootstyle="dark")
entry_save_path.pack(side="left", padx=5)
btn_save_path = ttk.Button(frame_save, text="Sfoglia", bootstyle=(INFO, "dark-outline"), style="primary", command=choose_save_path)
btn_save_path.pack(side="left")

# Frame per la scelta dell'immagine del logo
frame_logo = ttk.Frame(root)
frame_logo.pack(pady=5)

ttk.Label(frame_logo, text="Immagine del logo (opzionale):", font=("Helvetica", 12)).pack(anchor="w")
entry_logo_path = ttk.Entry(frame_logo, width=40, font=("Helvetica", 12), bootstyle="dark")
entry_logo_path.pack(side="left", padx=5)
btn_logo = ttk.Button(frame_logo, text="Sfoglia", bootstyle=(INFO, "dark-outline"), style="primary", command=choose_logo)
btn_logo.pack(side="left")

# Bottone per generare il QR code
btn_generate = ttk.Button(root, text="Genera QR Code", bootstyle="dark-outline", style="primary", command=generate_qr_code)
btn_generate.pack(pady=15, ipadx=10, ipady=5)

# Label per visualizzare il QR Code
label_qr = ttk.Label(root, text="⬇ Il tuo QR Code apparirà qui ⬇", font=("Helvetica", 10, "italic"))
label_qr.pack(pady=10)

# Footer
footer = ttk.Label(root, text="Made by Poppity", font=("Helvetica", 10), bootstyle=INFO)
footer.pack(side="bottom", pady=10)

# Avvio della GUI
root.mainloop()
