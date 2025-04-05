

import os
import base64
import hashlib
import pandas as pd
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet

file_path = []
encrypted_img = []
key = []

OUT_FOLDER = "D:/Info 3/SSI/Proiect/Date_trimis_primit"
SECRET_FILE_DEST = "D:/Info 3/SSI/Proiect/Cod/Fisier_secret_dest"
SECRET_FILE_EXP = "D:/Info 3/SSI/Proiect/Cod/Fisier_secret_exp"
IMAGE_FOLDER = "D:/Info 3/SSI/Proiect/Date/Date"

def export_public_key_expeditor():
    try:
        with open(os.path.join(SECRET_FILE_EXP, "expeditor_public_key.txt"), "rb") as f:
            public_key_data = f.read()
        with open(os.path.join(OUT_FOLDER, "expeditor_public_key.txt"), "wb") as f_out:
            f_out.write(public_key_data)
    except Exception as e:
        messagebox.showerror("Eroare export", f"Nu s-a putut exporta cheia publica a expeditorului:\n{e}")

def sign(message, private_key):
    return private_key.sign(
        message,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )

def sign_document():
    try:
        csv_path = os.path.join(OUT_FOLDER, "key_log.csv")
        with open(csv_path, "rb") as f:
            csv_data = f.read()
        with open(os.path.join(SECRET_FILE_EXP, "expeditor_private_key.txt"), "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)

        signature = sign(csv_data, private_key)

        with open(os.path.join(OUT_FOLDER, "key_log_signature.txt"), "w") as f:
            f.write(base64.b64encode(signature).decode())

        messagebox.showinfo("Semnare", "Fisierul a fost semnat cu succes.")
    except Exception as e:
        messagebox.showerror("Eroare semnare", f"Eroare la semnare: {e}")

def encrypt_public(message, public_key):
    return public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def load_image():
    global file_path
    file_path = filedialog.askopenfilenames(
        title="Selecteaza imagine(a)",
        initialdir=IMAGE_FOLDER,
        filetypes=[("Imagini BMP", "*.bmp")]
    )
    if file_path:
        messagebox.showinfo("Fisier(e) selectat(e)", "\n".join(file_path))
    return file_path

def crypt_image(file_path_list):
    global encrypted_img, key
    encrypted_img.clear()
    key.clear()

    for i, path in enumerate(file_path_list):
        with open(path, "rb") as f:
            img_bytes = f.read()

        current_key = Fernet.generate_key()
        fernet = Fernet(current_key)
        enc_img = fernet.encrypt(img_bytes)

        encrypted_img.append(enc_img)
        key.append(current_key)

        with open(os.path.join(OUT_FOLDER, f"encrypted_{i}.bin"), "wb") as f:
            f.write(enc_img)

        messagebox.showinfo("Succes", f"Imaginea {os.path.basename(path)} a fost criptata.")
    return encrypted_img, key

def generate_files():
    if not key or not encrypted_img:
        messagebox.showerror("Eroare", "Nu exista imagini criptate.")
        return

    with open(os.path.join(SECRET_FILE_DEST, "destinatar_public_key.txt"), "rb") as f:
        public_key_destinatar = serialization.load_pem_public_key(f.read())

    key_log = []
    for i in range(len(file_path)):
        key_encrypt = encrypt_public(key[i], public_key_destinatar)

        sha256 = hashlib.sha256()
        sha256.update(encrypted_img[i])
        hash_enc = sha256.hexdigest()

        with open(file_path[i], "rb") as f:
            img_bytes = f.read()
        sha256 = hashlib.sha256()
        sha256.update(img_bytes)
        hash_orig = sha256.hexdigest()

        encrypted_b64 = base64.b64encode(key_encrypt).decode()

        key_log.append({
            "image_name": os.path.basename(file_path[i]),
            "encrypted_key": encrypted_b64,
            "hash_img_encrypt": hash_enc,
            "hash_img_original": hash_orig,
        })

    df = pd.DataFrame(key_log)
    df.to_csv(os.path.join(OUT_FOLDER, "key_log.csv"), index=False)
    messagebox.showinfo("Transmitere", "Fisierele au fost generate si salvate.")