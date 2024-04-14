import os
from unittest.mock import patch

from common.tests import MediaTestCase
from signing.backend.handlers import EncryptFileHandler
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from app.settings import BASE_DIR
from ttp.backend.factories import RSAKeyFactory


class TestEncryptFile(MediaTestCase):
    MEDIA_DIR = os.path.join(BASE_DIR, 'tests', 'media')

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass(cls)
        RSAKeyFactory().create(key_name='test', directory=cls.MEDIA_DIR)

    @patch('PyQt6.QtWidgets.QFileDialog.getSaveFileName', return_value=(os.path.join(BASE_DIR, 'tests', 'media', 'encrypted_test.txt'), 'All Files (*)'))
    def test_encrypt_file(self, mock_getSaveFileName):
        file_content = b'Test message'
        file_path = os.path.join(self.MEDIA_DIR, 'test.txt')
        encrypted_file_path = os.path.join(self.MEDIA_DIR, 'encrypted_test.txt')

        with open(file_path, 'wb') as f:
            f.write(file_content)

        success = EncryptFileHandler.encrypt_file(file_path, os.path.join(self.MEDIA_DIR, 'test_rsa_public_key.pem'))

        self.assertTrue(success)
        self.assertTrue(os.path.exists(encrypted_file_path))

        with open(encrypted_file_path, 'rb') as f:
            encrypted_content = f.read()

        with open(os.path.join(self.MEDIA_DIR, 'test_rsa_private_key.pem'), 'rb') as f:
            private_key = RSA.import_key(f.read())

        cipher_rsa = PKCS1_OAEP.new(private_key)
        decrypted_content = cipher_rsa.decrypt(encrypted_content)

        self.assertEqual(decrypted_content, file_content)
