import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class PasswordManager:
    def __init__(self, master_password):
        self.salt = os.urandom(16)
        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=480000,
        )
        self.key = base64.urlsafe_b64encode(self.kdf.derive(master_password))
        self.fernet = Fernet(self.key)
        self.passwords = {}

    def add_password(self, service, password):
        encrypted_password = self.fernet.encrypt(password.encode())
        self.passwords[service] = encrypted_password

    def get_password(self, service):
        encrypted_password = self.passwords.get(service)
        if encrypted_password is None:
            return None
        return self.fernet.decrypt(encrypted_password).decode()

# Usage
password_manager = PasswordManager(b"master_password")
password_manager.add_password("email", "my_email_password")
print(password_manager.get_password("email"))
