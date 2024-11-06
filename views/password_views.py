import string
import secrets
import base64
import hashlib
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken

class FernetHasher:
    RANDOM_STRING_CHARS = string.ascii_lowercase + string.ascii_uppercase
    BASE_DIR = Path(__file__).resolve().parent.parent
    KEY_DIR = BASE_DIR / 'keys' 

    def __init__(self, key):
        if not isinstance(key, bytes):
            key = key.encode()

        self.fernet = Fernet(key)

    @classmethod
    def _get_random_string(cls, length=25):
        return ''.join(secrets.choice(cls.RANDOM_STRING_CHARS) for _ in range(length))

    @classmethod
    def create_key(cls, archive=False):
        value = cls._get_random_string()
        hasher = hashlib.sha256(value.encode('utf-8')).digest()
        # Codifique a hash de forma segura
        key = base64.b64encode(hasher).decode('utf-8')  # Decodifique para string para armazenamento
        if archive:
            return key, cls.archive_key(key.encode('utf-8'))  # Codifique a chave antes de gravar
        return key, None

    @classmethod
    def archive_key(cls, key):
        file_name = 'key.key'
        while (cls.KEY_DIR / file_name).exists():
            file_name = f'key_{cls._get_random_string(5)}.key'

        with open(cls.KEY_DIR / file_name, 'wb') as arquivo:
            arquivo.write(key)
        return cls.KEY_DIR / file_name

    def encrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode()

        return self.fernet.encrypt(value)

    def decrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode()
        try:
            return self.fernet.decrypt(value).decode()  # Corrigido
        except InvalidToken:
            return 'Token Invalido'

if __name__ == "__main__":
    pass
    # token gerado, chave
    #fernet_teste = FernetHasher('KnLxX5n+mMwvOVcFthH26BZFGYsroKmj5ikCfQHTd5c=')
    
    #Criptografa
    #print(fernet_teste.encrypt('senha123'))

    #Decriptografa
    #print(fernet_teste.decrypt('gAAAAABnKUtXryBSZqkBGY2SmYMe7jRMLSkZGynG_ZdmRvYhqTkWTSSfO9axrBc9V6talSlyx_KFNRsdQ73SnCvFaq9Kw5v6XA=='))