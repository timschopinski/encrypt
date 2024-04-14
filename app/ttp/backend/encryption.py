import os
from Crypto.Cipher import AES
from hashlib import sha256


class PrivateKeyEncryptor:
    @staticmethod
    def encrypt(private_key_path: str, directory: str, pin: str) -> None:
        with open(private_key_path, 'rb') as private_key_file:
            private_key_data = private_key_file.read()

        aes_key = sha256(pin.encode()).digest()
        cipher_aes = AES.new(aes_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(private_key_data)

        key_without_extension = os.path.splitext(os.path.basename(private_key_path))[0].replace('_private_key', '')
        encrypted_private_key_path = f'{key_without_extension}_encrypted_private_key.bin'

        with open(os.path.join(directory, encrypted_private_key_path), 'wb') as encrypted_key_file:
            [encrypted_key_file.write(x) for x in (cipher_aes.nonce, tag, ciphertext)]
