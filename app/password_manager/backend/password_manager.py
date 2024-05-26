from common.backend.utils import get_decrypted_private_key
from password_manager.backend.exceptions import PasswordLookupError
from Crypto.Cipher import PKCS1_OAEP


class PasswordManager:
    def __init__(self, encrypted_private_key_path: str):
        self.encrypted_private_key_path = encrypted_private_key_path

    def lookup(self, file: str, pin: str) -> str:
        private_key = get_decrypted_private_key(self.encrypted_private_key_path, pin, PasswordLookupError())
        with open(file, 'rb') as f:
            ciphertext = f.read()

        cipher_rsa = PKCS1_OAEP.new(private_key)
        plaintext = cipher_rsa.decrypt(ciphertext)

        return plaintext.decode('utf-8')
