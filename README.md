# SSI_Ionela_Bogdan_Crypt-Decrypt_image

## Cuprins
- [Scop](#Scop)
- [Etapele proiectului](#Etapele-proiectului)
- [Procesul de criptare](#Procesul-de-criptare)
- [Procesul de decriptare](#Procesul-de-decriptare)
- [Interfata grafica](#Interfata-grafica)
- [Tehnologii si concepte criptografice utilizate](#Tehnologii-si-concepte-criptografice-utilizate)
- [Anexa 1](#Anexa-1)
- [Bibliografie](#bibliografie)
## Scop
   Principalul obiectiv al proiectului constă în implementarea corectă și eficientă a conceptelor esențiale din domeniul securității informatice: confidențialitatea, integritatea, și non-repudierea.
   Proiectul se axează pe securizarea transmiterii unor imagini, folosind criptarea simetrică (Fernet) și criptarea asimetrică (RSA). În plus, imaginilor criptate li se aplică și funcția hash (SHA256) pentru a proteja conținutul și a asigura integritatea acestora.
   Pentru sporirea securității și minimizarea riscului interceptării datelor în procesul de transmitere, cheile utilizate pentru criptarea simetrică sunt, la rândul lor, criptate prin intermediul criptării asimetrice RSA, iar documentul rezultat este semnat digital.

---
## Etapele proiectului
  ### Procesul de criptare
   Funcțiile utilizate sunt interdependente, dar organizate clar astfel încât să reflecte succesiunea logică a operațiilor necesare securizării fișierelor de tip imagine.
   Centrul procesului de criptare este reprezentat de funcția crypt() care coordonează toate celelalte funcții implicate în criptarea imaginilor, generarea logului, semnarea digitală și exportul cheii publice. Aceasta funcționează ca un hub central de unde sunt lansate în ordine toate etapele esențiale.
   Funcțiile apelate în cadrul crypt() sunt următoarele:
- load_image()
	- deschidere dialog grafic (filedialog.askopenfilenames) ce permite selectarea fisierelor .bmp [1]
	- căile fisierelor selectate sunt stocate într-o listă ce va fi ulterior folosită în etapele ulterioare
- crypt_image(file_path_list) 
  	- citire conținut poze în bytes
  	- generare cheie Fernet pentru fiecare imagine în parte (criptare simetrică)
  	- criptare conținut imagine folosind cheia simetrică generată
  	- salvare imaginea criptată ca și fișier .bin
  	- cheia și imaginea criptată sunt salvate în listele globale key și encrypt
Această funcție este responsabilă direct de criptarea fișierelor de intrare. 
- generate_files() [2]
	- criptare chei Fernet folosind cheia publică (s-a folosit RSA-OAEP)
 	- calculare a doua hash-uri SHA256 pentru fiecare imagine (versiunea originală+versiunea criptată)
	- creare DataFrame (pandas) cu informațiile necesare (nume_fișier, cheia_criptată, hash-uri)
	- salvare informații intr-un fișier .csv (key_log.csv)
	- sign_document() [3, 4]
   	- încărcare fișier key_log.csv[5, 6] și cheia private a expeditorului
	- apelează sign() pentru semnarea conținutului fișierului
   	- salvare semnătură digitală într-un fișier key_log_signature.txt (Base64-encoded) [7]
- export_key_public_expeditor() – funcție care copiază cheia publică a expeditorului din folderul de configurare și o salvează în directorul de ieșire (OUT_FOLDER), pentru a fi trimisă destinatarului.
  	- utilizată pentru verificarea semnăturii digitale.
Funcții auxiliare în procesul de criptare:
- sign(message,private_key)  – funcție folosită pentru semnarea digitală și returnează semnătura digitală PSS (Probabilistic Signature Scheme) generate cu SHA256
	- primește o cheie RSA privată
 	- dencrypt_public (message,public_key) – funcție care criptează un mesaj (cheia Fernet)[8]
	- se utilizează criptarea asimetrică RSA și padding OAEP
   	- utilizată în generare_fișiere() pentru protejarea cheilor simetrice

  
---
  ### Procesul de decriptare
   Funcțiile sunt organizate clar, respectând succesiunea logică necesară pentru validarea semnăturii, verificarea integrității fișierelor și decriptarea conținutului acestora.
   Centrul procesului de decriptare este reprezentat de funcția decrypt_and_validate() care coordonează toate celelalte funcții implicate în verificarea semnăturii digitale, încărcarea cheii private, procesarea fișierului CSV, decriptarea fișierelor criptate și afișarea imaginilor originale. 
   Etapele procesului de decriptare și funcțiile utilizate sunt următoarele:
- verify_signature() – verificare semnătura digitală a fișierului key_log.csv
  	- incărcare semnătura digital și decodarea acesteia în Base64
  	- citire conținut și încărcare cheie publică expeditor
  	- utilizarea algoritmului RSA-PSS cu SHA256 pentru verificare
  	- verificare semnătură
  Se asigură autenticitatea expeditorului și integritatea.
- verify_file_integrity(private_key, df) – funcție pentru validare imaginilor criptate
  	- parcurgere fișier binar (.bin) primit 
  	- calculare hash SHA256 al imaginii criptate și comparare cu valoarea din key_log.csv
  	- succes – decodare cheie Fernet (Base64) și decriptare cu cheia folosind OAEP cu SHA256
  	- eroare – fișierul binar a fost corupt se oprește procesul de decritare
  	- decriptare imagine cu cheia Fernet
  	- recalculare hash pentru imaginea decriptată și se compară cu hash-ul original din csv
  	- imaginea este considerate validă și este adăugată în lista fișiere_valide
  Se verifică astfel integritatea imaginii criptate, căt și autenticitatea imaginii originale
- ecrypt_and_show_image(fișiere_valide)
  	- încărcare conținut imagine (Image.open) [9]
  	- validare format intern (image,verify()) 
  	- reîncărcare imagine și afișare pe ecran
  	- salvare imagini în fișierul DECRYPT_FOLDER
  	- afișare mesaj de succes în interfață
  
---
## Anexa 1
<img src="./images/Anexa 1. Schemă procese.png" alt="Eroare" width="600"/>

  ### Interfata grafica
   Pentru a facilita interacțiunea utilizatorului cu aplicația, proiectul include o interfață grafică dezvoltată cu ajutorul bibliotecii Tkinter, integrată direct în aplicație. Aceasta oferă un mod intuitiv și accesibil de a accesa funcționalitățile cheie ale aplicației, fără a necesita rularea scripturilor din linia de comandă.
   Interfața este organizată în jurul a patru funcționalități principale:
  - Criptare imagini – crypt()
  - Decriptare imagini – decrypt()
  - Resetare aplicație
  - Generare chei – generate_key()
  - Corupere fișier – alterate_file()
----
<h3>Interfața principală</h3>

<img src="./images/Interfata.png" alt="Interfața principală" width="600"/>

---

<h3>Resetarea aplicației</h3>

<img src="./images/Reset.png" alt="Resetare aplicație" width="600"/>

---

<h3>Generarea cheilor RSA</h3>

<img src="./images/Generare_chei_RSA.png" alt="Generare chei RSA" width="600"/>

---

<h3>Selectarea unei imagini pentru criptare</h3>

<img src="./images/Criptare_selectare_img.png" alt="Selectare imagine" width="600"/>

---

<h3>Confirmare imagine selectată</h3>

<img src="./images/Criptare_mesaj_poza_selectata.png" alt="Imagine selectată pentru criptare" width="600"/>

---

<h3>Confirmare criptare reușită</h3>

<img src="./images/Criptare_mesaj_criptare_reusita.png" alt="Criptare reușită" width="600"/>

---
<h3>Fișier semnat cu succes</h3>
	
<img src="./images/Fisier_semnat_cu_sicces.png" alt="Fișier semnat digital cu succes" width="600"/>

---
<h3>Fișier pregătit pentru transmitere la receiver</h3>
	
<img src="./images/Fisier_prergatit_pt_trimis_la_receiver.png" alt="Fișier pregătit pentru transmitere" width="600"/>

---
<h3>Decriptare reușită - Mesaj validare</h3>
	
<img src="./images/Decriptare_mesaj.png" alt="Mesaj validare decriptare" width="600"/>

---
<h3>Decriptare reușită - Imagine validată și afișată</h3>
	
<img src="./images/Decriptare_mesaj+poza.png" alt="Imagine decriptată și validată" width="600"/>

---
<h3>Comparare imagine originală vs imagine criptată</h3>
	
<img src="./images/Comparare_img_originala_criptata.png" alt="Comparare imagine originală și criptată" width="600"/>

---
<h3>Alterare fișier binar</h3>
	
<img src="./images/Alterare_fisier_binar.png" alt="Fișier binar alterat" width="600"/>

---
<h3>Eroare la decriptare după alterarea fișierului</h3>
	
<img src="./images/Alterare_fisier_binar_la_decriptare_mesaj_de_eroare.png" alt="Eroare de integritate la decriptare" width="600"/>

---

## Tehnologii si concepte criptografice utilizate
   În realizarea acestui proiect au fost utilizate multiple tehnologii și algoritmi standard din domeniul securității informatice. Acestea contribuie împreună la asigurarea confidențialității, integrității și autenticității datelor transmise. Mai jos sunt descrise principalele instrumente și concepte aplicate:
 **Fernet (criptare simetrică)**
  - Folosit pentru criptarea propriu-zisă a fișierelor de tip imagine.
  - Fernet implementează AES în mod CBC (128-bit) cu un mecanism intern de autentificare (HMAC).
  - Oferă confidențialitate și integritate a datelor criptate într-un singur obiect criptografic.
  - Se generează o cheie Fernet unică pentru fiecare imagine.

- **OAEP (Optimal Asymmetric Encryption Padding)**
  - Algoritm de padding pentru criptarea cu RSA, rezistent la atacuri de tip padding oracle.
  - Utilizat în metoda `encrypt_public()` pentru criptarea cheilor Fernet.

- **RSA (criptare asimetrică)** [10]
  - Utilizat pentru criptarea cheilor simetrice Fernet.
  - Se aplică algoritmul RSA cu padding OAEP împreună cu funcția de hash SHA256.
  - Cheile RSA utilizate sunt în format PEM.
  - Asigură că doar destinatarul (care deține cheia privată) poate accesa cheia Fernet aferentă fiecărei imagini.

- **PSS (Probabilistic Signature Scheme)**
  - Algoritm utilizat pentru semnătura digitală în combinație cu RSA.
  - Oferă protecție împotriva atacurilor de tip adaptiv (chosen message attacks).
  - Implementat în funcția `sign()` pentru semnarea fișierului `key_log.csv`.

- **SHA256 (algoritm de hash)**
  - algoritm de amprentare criptografică folosit pentru:
    - hash-ul imaginii originale;
    - hash-ul imaginii criptate;
    - generarea semnăturii digitale.
  - utilizat pentru verificarea integrității fișierelor și pentru semnăturile digitale.

- **Base64 (codificare)**
  - mecanism de codificare binar-text, utilizat pentru a reprezenta date binare sub formă de șiruri de caractere text.
  - utilizat în:
    - codificarea cheilor Fernet criptate;
    - codificarea semnăturii digitale în fișierul `key_log_signature.txt`.

- **Serialization (încărcare chei criptografice)**
  - folosită pentru a încărca cheile RSA (private/publice).
  - funcțiile `serialization.load_pem_private_key()` și `serialization.load_pem_public_key()` din modulul `cryptography` sunt utilizate pentru a converti fișierele `.txt` ce conțin chei în obiecte criptografice funcționale. [11]

- **Pandas (manipulare fișiere CSV)**
  - bibliotecă Python utilizată pentru a crea și salva tabelul `key_log.csv` sub formă de DataFrame.
  - permite stocarea organizată a:
    - numelui imaginii;
    - cheii criptate (Base64);
    - hash-urilor SHA256 aferente fiecărei imagini.

- **Tkinter (interfață grafică)**
  - biblioteca grafică nativă a limbajului Python.
  - utilizată pentru:
    - selectarea fișierelor `.bmp` din sistem;
    - afișarea de mesaje informative, de eroare sau succes;
    - interacțiunea cu utilizatorul în mod intuitiv.

---


---
## Bibliografie
[1] Python Software Foundation, (n.d.), *tkinter.simpledialog — Standard Tkinter input dialogs*, Python Documentation, [Accesat la 21.03.2025], [Link](https://docs.python.org/3/library/dialog.html)

[2] GeeksforGeeks, (n.d.), *How to read from a file in Python*, GeeksforGeeks, [Accesat 2 aprilie 2025], [Link](https://www.geeksforgeeks.org/how-to-read-from-a-file-in-python/)

[3] Python Cryptographic Authority, (n.d.), *Serialization — Cryptography 3.4.5 documentation*, Cryptography.io, [Accesat la 21.03.2025], [Link](https://cryptography.io/en/3.4.5/hazmat/primitives/asymmetric/serialization.html)

[4] GeeksforGeeks, (n.d.), *Encoding and decoding Base64 strings in Python*, GeeksforGeeks, [Accesat la 2 aprilie 2025], [Link](https://www.geeksforgeeks.org/encoding-and-decoding-base64-strings-in-python/)

[5] Reddit user /u/[autor necunoscut], (2022), *How to iterate through a pandas dataframe csv*, Reddit, [Accesat la 21.03.2025], [Link](https://www.reddit.com/r/learnpython/comments/wbvjvl/how_to_iterate_through_a_pandas_dataframe_csv/)

[6] GeeksforGeeks, (n.d.), *Iterating over rows and columns in Pandas DataFrame*, GeeksforGeeks, [Accesat la 22.03.2025], [Link](https://www.geeksforgeeks.org/iterating-over-rows-and-columns-in-pandas-dataframe/)

[7] GeeksforGeeks, (n.d.), *Writing to file in Python*, GeeksforGeeks, [Accesat la 2 aprilie 2025], [Link](https://www.geeksforgeeks.org/writing-to-file-in-python/)

[8] ELC, (n.d.), *Asymmetric Encryption*, ELC GitHub, [Accesat la 22.03.2025], [Link](https://elc.github.io/python-security/chapters/07_Asymmetric_Encryption.html)

[9] Tech with Tim, (2020), *How to Reconstruct an Image using Python*, YouTube, [Accesat la 22.03.2025], [Link](https://www.youtube.com/watch?v=xZF6zWLz-vY)

[10] TechTalkWithAlex, (2023), *Cryptography in Python – A practical example to code*, Medium, [Accesat la 22.03.2025], [Link](https://medium.com/@TechTalkWithAlex/cryptography-in-python-a-pracAStical-example-to-code-2899b9bd176c)

[11] Berry, A., (2021), *Generating Encrypted Key Pairs in Python*, DEV.to, [Accesat la 23.03.2025], [Link](https://dev.to/aaronktberry/generating-encrypted-key-pairs-in-python-69b)

