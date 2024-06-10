import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC #  Password-Based Key Derivation Function 2 with HMAC (Hash-Based Message Authentication Code)
password = b"password" # This will be used to generate a cryptographic key.
salt = os.urandom(16) # returns 16 random bytes suitable for cryptographic use.
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000,
)
key = base64.urlsafe_b64encode(kdf.derive(password))
f = Fernet(key)
token = f.encrypt(b"Secret message!")

