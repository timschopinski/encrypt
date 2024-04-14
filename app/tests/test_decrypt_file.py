import os
from unittest.mock import patch
from common.tests import MediaTestCase
from signing.backend.handlers import DecryptFileHandler
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from app.settings import BASE_DIR
from ttp.backend.factories import RSAKeyFactory


class TestDecryptFile(MediaTestCase):
    MEDIA_DIR = os.path.join(BASE_DIR, 'tests', 'media')

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass(cls)
        RSAKeyFactory().create(key_name='test', directory=cls.MEDIA_DIR)

    @patch('PyQt6.QtWidgets.QFileDialog.getSaveFileName', return_value=(os.path.join(BASE_DIR, 'tests', 'media', 'decrypted_test.txt'), 'All Files (*)'))
    def test_decrypt_file(self, mock_getSaveFileName):
        encrypted_file_path = os.path.join(self.MEDIA_DIR, 'encrypted_test.txt')
        original_message = b'xyz'

        with open(os.path.join(self.MEDIA_DIR, 'test_rsa_public_key.pem'), 'rb') as f:
            public_key = RSA.import_key(f.read())

        cipher_rsa = PKCS1_OAEP.new(public_key)
        encrypted_content = cipher_rsa.encrypt(original_message)

        with open(encrypted_file_path, 'wb') as f:
            f.write(encrypted_content)

        decrypted_file_path = os.path.join(self.MEDIA_DIR, 'decrypted_test.txt')
        success = DecryptFileHandler.decrypt_file(encrypted_file_path, os.path.join(self.MEDIA_DIR, 'test_rsa_private_key.pem'))

        self.assertTrue(success)
        self.assertTrue(os.path.exists(decrypted_file_path))

        with open(decrypted_file_path, 'rb') as f:
            decrypted_content = f.read()

        expected_decrypted_content = b'xyz'

        self.assertEqual(decrypted_content, expected_decrypted_content)
