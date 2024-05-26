from Crypto.Cipher import AES
from hashlib import sha256
from Crypto.PublicKey import RSA

from common.backend.exceptions import EncryptException


def get_decrypted_private_key(encrypted_private_key_path: str, pin: str, error: EncryptException):
    try:
        with open(encrypted_private_key_path, 'rb') as key_file:
            key_data = key_file.read()
            nonce = key_data[:16]
            tag = key_data[16:32]
            ciphertext = key_data[32:]
            cipher_aes = AES.new(sha256(pin.encode()).digest(), AES.MODE_EAX, nonce=nonce)
            private_key_data = cipher_aes.decrypt_and_verify(ciphertext, tag)

        return RSA.import_key(private_key_data)
    except Exception:
        raise error
