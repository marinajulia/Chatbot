import os
import json

from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

FERNET_KEY = os.getenv("FERNET_KEY")

fernet = Fernet(FERNET_KEY.encode())

def encrypt_data(data:dict)-> str:
    json_data = json.dumps(data)
    encrypted_data = fernet.encrypt(json_data.encode()).decode()
    return encrypted_data

def decrypt_data(data: str) -> dict:
    decrypted_data = fernet.decrypt(data.encode())
    data_json = json.loads(decrypted_data.decode())
    return data_json

data_encrypted = encrypt_data({"teste": "teste"})

print(data_encrypted)

data_decode = decrypt_data(data_encrypted)

print(data_decode)
