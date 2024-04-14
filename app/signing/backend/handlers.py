from Crypto.Cipher import PKCS1_OAEP
from common.backend.algorithms import RsaAlgorithm
from PyQt6.QtWidgets import QFileDialog


class EncryptFileHandler:
    @staticmethod
    def encrypt_file(file_path: str, public_key_path: str) -> bool:
        public_key = RsaAlgorithm.load_key(public_key_path)

        with open(file_path, 'rb') as f:
            plaintext = f.read()

        cipher_rsa = PKCS1_OAEP.new(public_key)
        ciphertext = cipher_rsa.encrypt(plaintext)

        encrypted_file_path, _ = QFileDialog.getSaveFileName(None, 'Save Encrypted File', '', 'All Files (*)')
        if encrypted_file_path:
            with open(encrypted_file_path, 'wb') as f:
                f.write(ciphertext)
            return True
        return False


class DecryptFileHandler:
    @staticmethod
    def decrypt_file(file_path: str, private_key_path: str) -> bool:
        private_key = RsaAlgorithm.load_key(private_key_path)

        with open(file_path, 'rb') as f:
            ciphertext = f.read()

        cipher_rsa = PKCS1_OAEP.new(private_key)
        plaintext = cipher_rsa.decrypt(ciphertext)

        decrypted_file_path, _ = QFileDialog.getSaveFileName(None, 'Save Decrypted File', '', 'All Files (*)')
        if decrypted_file_path:
            with open(decrypted_file_path, 'wb') as f:
                f.write(plaintext)
            return True
        return False
