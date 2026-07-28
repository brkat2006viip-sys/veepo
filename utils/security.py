import secrets
import string
from cryptography.fernet import Fernet

def generate_fernet_key() -> str:
    return Fernet.generate_key().decode()

def encrypt_value(fernet_key: str, value: str) -> str:
    f = Fernet(fernet_key.encode())
    return f.encrypt(value.encode()).decode()

def decrypt_value(fernet_key: str, token: str) -> str:
    f = Fernet(fernet_key.encode())
    return f.decrypt(token.encode()).decode()

def generate_random_name(prefix: str = "obj_", length: int = 8) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return prefix + ''.join(secrets.choice(alphabet) for _ in range(length))
