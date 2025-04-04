# SSI_Ionela_Bogdan_Crypt-Decrypt_image

## 📑 Cuprins
- [Descriere](#-descriere)
- [Funcționalități principale](#-funcționalități-principale)
- [Structura proiectului](#-structura-proiectului)
- [Tehnologii și concepte folosite](#-tehnologii-și-concepte-folosite)
- [Cum rulezi proiectul](#-cum-rulezi-proiectul)
- [Autori](#-autori)
- [Bibliografie](#-bibliografie)

---

## 📋 Descriere
Acest proiect are ca scop implementarea conceptelor de **securitate informatică**: **confidențialitate**, **integritate** și **non-repudiere**, prin securizarea transmiterii imaginilor folosind:
- Criptare simetrică (Fernet)
- Criptare asimetrică (RSA)
- Semnătură digitală (PSS)
- Hash-uri de verificare (SHA256)

Imaginile sunt criptate, semnate digital și verificate la destinație pentru a preveni accesul neautorizat și alterarea datelor.

---

## 🛠️ Funcționalități principale
- 🔒 Criptare imagini folosind chei Fernet generate dinamic
- 🔑 Criptare chei simetrice cu RSA + OAEP
- ✍️ Semnare digitală a fișierelor criptate
- 🔎 Verificare semnătură digitală și integritate imagini
- 🖼️ Afișare imagini decriptate în interfața grafică
- 🖥️ Interfață grafică intuitivă (Tkinter)

---

## 📂 Structura proiectului
- **crypt()** – Criptarea imaginilor și semnarea log-ului
- **decrypt_and_validate()** – Decriptarea și validarea imaginilor
- **generate_key()** – Generarea perechii de chei RSA
- **alterate_file()** – Coruperea intenționată a unui fișier pentru teste
- **Tkinter GUI** – Interfață grafică pentru utilizator

---

## 🧩 Tehnologii și concepte folosite
- **Fernet** (Criptare simetrică AES-CBC + HMAC)
- **RSA** cu **OAEP** (Criptare asimetrică chei Fernet)
- **PSS** (Semnătură digitală probabilistică)
- **SHA256** (Hash pentru integritate)
- **Base64** (Codificare binar-text)
- **Tkinter** (Interfață grafică)
- **Pandas** (Procesare fișiere CSV)

