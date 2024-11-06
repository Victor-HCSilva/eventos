import os
import sys
import base64
import hashlib
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
import json

class PasswordManager:
    BASE_DIR = Path(__file__).resolve().parent.parent
    CONFIG_DIR = BASE_DIR / 'config'
    CONFIG_FILE = CONFIG_DIR / 'config.json'

    def __init__(self):
        self.load_config()

    def load_config(self):
        if not self.CONFIG_DIR.exists():
            self.CONFIG_DIR.mkdir()
        if not self.CONFIG_FILE.exists():
            self.create_config()
        with open(self.CONFIG_FILE, 'r') as f:
            self.config = json.load(f)

    def create_config(self):
        self.config = {"key": self.generate_key()}
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(self.config, f)

    def generate_key(self):
        key = base64.urlsafe_b64encode(os.urandom(32))
        return key.decode()

    def save_password(self, domain, password):
        fernet = Fernet(self.config["key"].encode())
        encrypted_password = fernet.encrypt(password.encode()).decode()
        try:
            with open(self.CONFIG_DIR / 'passwords.json', 'r') as f:
                passwords = json.load(f)
        except FileNotFoundError:
            passwords = {}
        passwords[domain] = encrypted_password
        with open(self.CONFIG_DIR / 'passwords.json', 'w') as f:
            json.dump(passwords, f)
        print(f"Senha salva para o domínio {domain}")

    def get_password(self, domain):
        fernet = Fernet(self.config["key"].encode())
        try:
            with open(self.CONFIG_DIR / 'passwords.json', 'r') as f:
                passwords = json.load(f)
            if domain in passwords:
                encrypted_password = passwords[domain]
                decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()
                print(f"Senha para {domain}: {decrypted_password}")
            else:
                print(f"Nenhuma senha encontrada para o domínio {domain}")
        except FileNotFoundError:
            print(f"Nenhuma senha salva encontrada.")

if __name__ == "__main__":
    manager = PasswordManager()
    while True:
        action = input("Digite 1 para salvar uma senha, 2 para recuperar uma senha, ou 3 para sair: ")
        if action == '1':
            domain = input("Domínio: ")
            password = input("Senha: ")
            manager.save_password(domain, password)
        elif action == '2':
            domain = input("Domínio: ")
            manager.get_password(domain)
        elif action == '3':
            break
        else:
            print("Opção inválida.")
            