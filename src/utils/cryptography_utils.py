import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

class CryptographyUtils:
    def __init__(self):
        load_dotenv()
        self.fernet = Fernet(os.getenv('FERNET_KEY'))

    def encrypt(self, text):
        return self.fernet.encrypt(text.encode())

    def decrypt(self, text):
        return self.fernet.decrypt(text).decode()

