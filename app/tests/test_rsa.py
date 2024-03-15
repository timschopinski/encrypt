import os
from common.tests import MediaTestCase
from crypto.rsa import RSAKeys
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from settings import BASE_DIR


class TestRSAKeys(MediaTestCase):
    MEDIA_DIR = os.path.join(BASE_DIR, 'tests', 'media')

    @classmethod
    def setUpClass(cls) -> None:
        rsa_keys = RSAKeys(cls.MEDIA_DIR)
        key_name = 'test'
        rsa_keys.create(key_name)

        cls.private_key_path = os.path.join(cls.MEDIA_DIR, f'{key_name}_private_key.pem')
        cls.public_key_path = os.path.join(cls.MEDIA_DIR, f'{key_name}_public_key.pem')

    def test_rsa_keys_creates_keys(self):
        self.assertTrue(os.path.exists(self.private_key_path))
        self.assertTrue(os.path.exists(self.public_key_path))

    def test_rsa_keys(self):
        with open(self.private_key_path, 'rb') as private_key_file:
            private_key = RSA.import_key(private_key_file.read())
        with open(self.public_key_path, 'rb') as public_key_file:
            public_key = RSA.import_key(public_key_file.read())

        message = b"Test message"
        cipher_rsa = PKCS1_OAEP.new(public_key)
        encrypted = cipher_rsa.encrypt(message)
        cipher_rsa = PKCS1_OAEP.new(private_key)
        decrypted = cipher_rsa.decrypt(encrypted)

        self.assertEqual(decrypted, message)

    def test_rsa_encryption_with_wrong_key(self):
        with open(self.public_key_path, 'rb') as public_key_file:
            public_key = RSA.import_key(public_key_file.read())
        message = b"Test message"
        cipher_rsa = PKCS1_OAEP.new(public_key)
        encrypted = cipher_rsa.encrypt(message)
        wrong_private_key = RSA.generate(4096)
        cipher_rsa = PKCS1_OAEP.new(wrong_private_key)
        with self.assertRaises(ValueError):
            cipher_rsa.decrypt(encrypted)
