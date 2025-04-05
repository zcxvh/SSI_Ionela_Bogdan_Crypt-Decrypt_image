

import tkinter as tk
from tkinter import messagebox
from tkinter import *
from cryptography.hazmat.primitives import serialization
import base64
import os
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
import hashlib
from PIL import Image
import io
from cryptography.fernet import Fernet
from Encrypt import *
from PIL import UnidentifiedImageError

SECRET_FILE_DEST="D:/Info 3/SSI/Proiect/Cod/Fisier_secret_dest"
SEND_RECEIVE_FILE="D:/Info 3/SSI/Proiect/Date_trimis_primit"
DECRYPT_FOLDER="D:/Info 3/SSI/Proiect/Imagini_Decriptate"

def verify_signature():
    try:
        with open(os.path.join(SEND_RECEIVE_FILE, "key_log_signature.txt"), "r") as f:
            signature_b64 = f.read()
        signature = base64.b64decode(signature_b64)

        csv_path = os.path.join(SEND_RECEIVE_FILE, "key_log.csv")
        with open(csv_path, "rb") as f:
            csv_data = f.read()

        with open(os.path.join(SEND_RECEIVE_FILE, "expeditor_public_key.txt"), "rb") as f:
            public_key_expeditor = serialization.load_pem_public_key(f.read())

        public_key_expeditor.verify(
            signature,
            csv_data,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        messagebox.showerror("Semnatura", "Semnatura este invalida.")
        return False
    except Exception as e:
        messagebox.showerror("Eroare", f"Eroare la verificarea semnaturii:\n{e}")
        return False

def load_key_private_receiver():
    try:
        with open(os.path.join(SECRET_FILE_DEST, "destinatar_private_key.txt"), "rb") as f:
            return serialization.load_pem_private_key(f.read(), password=None)
    except Exception as e:
        messagebox.showerror("Eroare", f"Nu s-a putut incarca cheia privata:\n{e}")
        return None
    
def verify_file_integrity(private_key, df):
    fisiere_valide = []
    for filename in os.listdir(SEND_RECEIVE_FILE):
        if filename.endswith(".bin"):
            path = os.path.join(SEND_RECEIVE_FILE, filename)
            with open(path, 'rb') as f:
                encrypted_data = f.read()

            sha256 = hashlib.sha256()
            sha256.update(encrypted_data)
            hash_calculat = sha256.hexdigest()

            for row in df.iterrows():
                if hash_calculat == row["hash_img_encrypt"]:
                    
                        encrypted_key = base64.b64decode(row["encrypted_key"])
                        key = private_key.decrypt(
                            encrypted_key,
                            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                         algorithm=hashes.SHA256(), label=None)
                        )
                        fernet = Fernet(key)
                        decrypted_data = fernet.decrypt(encrypted_data)

                        sha256 = hashlib.sha256()
                        sha256.update(decrypted_data)
                        hash_original = sha256.hexdigest()

                        if hash_original == row["hash_img_original"]:
                            fisiere_valide.append((filename, decrypted_data))
                        else:
                            raise Exception("Hash original diferit")
                        break
            else:
                messagebox.showerror("Eroare", f"{filename} nu se regaseste in log.")
                return []
    print(f"Adaugat in fisiere_valide: {filename}, {len(decrypted_data)} bytes")
    return fisiere_valide

def decrypt_and_show_image(fisiere_valide):
    for nume, data in fisiere_valide:
        try:
            image = Image.open(io.BytesIO(data))
            image.verify()  # verifica integritatea imaginii 
            image = Image.open(io.BytesIO(data))  # reincarcare imagine pentru afisare 
            image.show()
            os.makedirs(DECRYPT_FOLDER, exist_ok=True)
            nume_fara_ext = os.path.splitext(nume)[0]
            cale_salvare = os.path.join(DECRYPT_FOLDER, f"{nume_fara_ext}_decrypted.bmp")
            image.save(cale_salvare)
            messagebox.showinfo("Validare", f"{nume} este valid si a fost salvat la:\n{cale_salvare}")
        except UnidentifiedImageError:
            messagebox.showerror("Imagine invalida", f"{nume} nu este o imagine BMP valida.")
        except Exception as e:
            messagebox.showerror("Eroare afisare", f"{nume} nu a putut fi afisata:\n{str(e)}")