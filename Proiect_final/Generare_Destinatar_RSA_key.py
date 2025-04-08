


from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def generate_key_pair():
    key_size = 2048  

    private_key = rsa.generate_private_key(
        public_exponent=65537, 
        key_size=key_size,
    )
    public_key = private_key.public_key()

    #--------------------------------------------
    private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    #------------------------------------------------------

    with open("D:/Info 3/SSI/Proiect/Cod/Fisier_secret_dest/destinatar_private_key.txt", "wb") as f:
        f.write(private_pem)

    with open("D:/Info 3/SSI/Proiect/Cod/Fisier_secret_dest/destinatar_public_key.txt", "wb") as f:
        f.write(public_pem)
    #---------------------------------------------------------

    return private_key, public_key

if __name__ == "__main__":
    private_key, public_key = generate_key_pair()