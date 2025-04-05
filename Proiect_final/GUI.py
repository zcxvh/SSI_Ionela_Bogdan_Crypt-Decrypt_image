


import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import *
from tkinter import filedialog
import os
import pandas as pd
from PIL import Image
import io
from Generare_Destinatar_RSA_key import generate_key_pair
from Generare_Expeditor_RSA_key import generate_key_pair_exp
from Encrypt import *
from Encrypt import key, encrypted_img
from Decrypt import *

file_path=None
img_bytes=None
OUT_FOLDER="D:/Info 3/SSI/Proiect/Date_trimis_primit"
SECRET_FILE_DEST="D:/Info 3/SSI/Proiect/Cod/Fisier_secret_dest"
SECRET_FILE_EXP="D:/Info 3/SSI/Proiect/Cod/Fisier_secret_exp"
SEND_RECEIVE_FILE="D:/Info 3/SSI/Proiect/Date_trimis_primit"
IMAGE_FOLDER="D:/Info 3/SSI/Proiect/Date/Date"
DECRYPT_FOLDER="D:/Info 3/SSI/Proiect/Imagini_Decriptate"

##### CRIPTARE
def crypt():
    file_path=load_image()
    crypt_image(file_path)
    generate_files()
    sign_document()
    export_public_key_expeditor()

def reset():
    try:
        #stergere din OUT_FOLDER
        for filename in os.listdir(OUT_FOLDER):
            path = os.path.join(OUT_FOLDER, filename)
            if os.path.isfile(path):
                os.remove(path)
        # stergere din SECRET_FILE_DEST
        for filename in os.listdir(SECRET_FILE_DEST):
            path = os.path.join(SECRET_FILE_DEST, filename)
            if os.path.isfile(path):
                os.remove(path)
        # stergere din SECRET_FILE_EXP
        for filename in os.listdir(SECRET_FILE_EXP):
            path = os.path.join(SECRET_FILE_EXP, filename)
            if os.path.isfile(path):
                os.remove(path)
        for filename in os.listdir(DECRYPT_FOLDER):
            path = os.path.join(DECRYPT_FOLDER, filename)
            if os.path.isfile(path):
                os.remove(path)

        # Reset variabile globale
        encrypted_img.clear()
        key.clear()
        btn_gen_chei.config(state=tk.NORMAL)     # reactivare buton chei
        messagebox.showinfo("Resetare", "Toate fisierele si variabilele au fost resetate.")
    except Exception as e:
        messagebox.showerror("Eroare", f"Eroare la resetare:\n{str(e)}")
       
def generate_key(buton):
    generate_key_pair_exp()
    generate_key_pair()
    buton.config(state=tk.DISABLED)

def alterate_file(byte_location=2000, new_bytes=b"TEST"):
    try:
        # selectare fisier binar
        original_file = filedialog.askopenfilename(
            title="Selecteaza fisierul binar de corupt",
            initialdir=SEND_RECEIVE_FILE,
            filetypes=[("Fisiere binare", "*.bin")]
        )
        if not original_file:
            return  # anulare
        with open(original_file, 'r+b') as f:
            f.seek(byte_location)
            f.write(new_bytes)    
        messagebox.showinfo("Modificare", "Fisierul a fost modificat cu succes.")    
    except Exception as e:
        messagebox.showerror("Eroare", f"A aparut o eroare la corupere:\n{e}")
    
##### DECRIPTARE
def decrypt_and_validate():
    try:
        verify_signature()
        private_key = load_key_private_receiver()
        if private_key is None:
            return
        df = pd.read_csv(os.path.join(SEND_RECEIVE_FILE, "key_log.csv"))
        fisiere_valide = verify_file_integrity(private_key, df)
        decrypt_and_show_image(fisiere_valide)
    except Exception as e:
        messagebox.showerror("Eroare", f"A aparut o eroare:\n{str(e)}")

def check_all_bin_images():
    try:
        for filename in os.listdir(SEND_RECEIVE_FILE):
        
                filepath = os.path.join(SEND_RECEIVE_FILE, filename)
                with open(filepath, 'rb') as f:
                    data = f.read()
                    try:
                        image = Image.open(io.BytesIO(data))
                        image.verify() 
                        image.show()
                    except Exception as e:
                        print(f"Fisierul {filename} NU este imagine valida: {e}")
    except Exception as e:  
        messagebox.showerror("Eroare", f"A aparut o eroare:\n{str(e)}")

# fereastra principala
root = tk.Tk()
root.title("Interfata GUI - Securitate Imagine")
root.geometry("900x900")
root.resizable(False, False)

# Layout: 3 coloane
frame_expeditor = tk.Frame(root, padx=10, pady=10, relief=tk.GROOVE, bd=2)
frame_comun = tk.Frame(root, padx=10, pady=10, relief=tk.GROOVE, bd=2)
frame_destinatar = tk.Frame(root, padx=10, pady=10, relief=tk.GROOVE, bd=2)

frame_expeditor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
frame_comun.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
frame_destinatar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Titluri
tk.Label(frame_expeditor, text="Sender", font=('Arial', 12, 'bold')).pack(pady=5)
tk.Label(frame_comun, text="Settings", font=('Arial', 12, 'bold')).pack(pady=5)
tk.Label(frame_destinatar, text="Receiver", font=('Arial', 12, 'bold')).pack(pady=5)

# Butoane Expeditor
tk.Button(frame_expeditor, text="Crypt", command=crypt, width=30).pack(pady=5)
tk.Button(frame_comun, text="Alterate binary file", command=alterate_file, width=30).pack(pady=5)
# Butoane Comune
tk.Button(frame_comun, text="Reset", command=reset, width=30).pack(pady=15)
btn_gen_chei = tk.Button(frame_comun, text="Generate RSA key", width=30)
btn_gen_chei.pack(pady=5)
btn_gen_chei.config(command=lambda: generate_key(btn_gen_chei))

# Butoane Destinatar
tk.Button(frame_destinatar, text="Decrypt and validate", command=decrypt_and_validate, width=30).pack(pady=40)

root.mainloop()