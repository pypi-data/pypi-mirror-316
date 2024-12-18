from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import os


def generate_aes_key() -> str:
    key = os.urandom(32)  # 256-bit key
    return base64.b64encode(key).decode()


def Aencrypt(data: str, secret_key: str) -> str:
    decoded_key = base64.b64decode(secret_key)
    cipher = Cipher(algorithms.AES(decoded_key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(AES.block_size).padder()
    padded_data = padder.update(data.encode('utf-8')) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(encrypted_data).decode('utf-8')


def Adecrypt(encrypted_data: str, secret_key: str) -> str:
    decoded_key = base64.b64decode(secret_key)
    cipher = Cipher(algorithms.AES(decoded_key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()

    encrypted_data_bytes = base64.b64decode(encrypted_data)
    decrypted_padded_data = decryptor.update(encrypted_data_bytes) + decryptor.finalize()

    unpadder = padding.PKCS7(AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    return decrypted_data.decode('utf-8')
