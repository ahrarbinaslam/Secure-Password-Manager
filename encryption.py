import os
import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

salt_size= 16
key_size= 32
iterations = 10000

def generate_key(password:str, salt:bytes) -> bytes:
    return PBKDF2(password, salt, dkLen=key_size, count=iterations)

def encrypt_password(password: str, key: bytes) -> str:
    cipher = AES.new(key, AES.MODE_GCM)
    cipher_text, tag = cipher.encrypt_and_digest(password.encode())
    encrypted_data = base64.b64encode(cipher.nonce + tag + cipher_text).decode()
    return encrypted_data


def decrypt_password(encrypted_password: str, key: bytes) -> str:
        data = base64.b64decode(encrypted_password, validate=True) 
        nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode()
