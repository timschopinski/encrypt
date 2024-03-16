from PyQt6.QtWidgets import QPushButton, QMessageBox, QLineEdit, QLabel
from crypto.rsa import RSAKeys
import os
from Crypto.Cipher import AES
from hashlib import sha256
from gui.base import BaseWindow


class TTPWindow(BaseWindow):
    window_title = 'TTP Application'

    def initUI(self):
        super().initUI()

        self.key_name_input = QLineEdit(self)
        self.layout.addWidget(QLabel('Enter name for RSA keys (without extension):'))
        self.layout.addWidget(self.key_name_input)

        self.generate_keys_button = QPushButton('Generate RSA Keys', self)
        self.generate_keys_button.clicked.connect(self.generate_rsa_keys)
        self.layout.addWidget(self.generate_keys_button)

        self.encrypt_key_button = QPushButton('Encrypt Private Key', self)
        self.encrypt_key_button.clicked.connect(self.encrypt_private_key)
        self.layout.addWidget(self.encrypt_key_button)

        self.pin_input = QLineEdit(self)
        self.layout.addWidget(QLabel('Enter User A PIN:'))
        self.layout.addWidget(self.pin_input)

    def generate_rsa_keys(self):
        key_name = self.key_name_input.text()
        if not key_name:
            QMessageBox.warning(self, 'Empty Key Name', 'Please enter a name for the RSA keys.')
            return

        rsa_keys = RSAKeys()
        rsa_keys.create(key_name)
        QMessageBox.information(self, 'Success', 'RSA Keys Generated.')

    def encrypt_private_key(self):
        pin = self.pin_input.text()
        if not pin:
            QMessageBox.warning(self, 'Empty PIN', 'Please enter a PIN.')
            return

        key_name = self.key_name_input.text()
        if not key_name:
            QMessageBox.warning(self, 'Empty Key Name', 'Please enter a name for the RSA keys.')
            return

        private_key_path = f'{key_name}_private_key.pem'
        if not os.path.exists(private_key_path):
            QMessageBox.warning(self, 'Private Key Not Found', 'Private key not found. Generate RSA keys first.')
            return

        with open(private_key_path, 'rb') as private_key_file:
            private_key_data = private_key_file.read()

        aes_key = sha256(pin.encode()).digest()

        cipher_aes = AES.new(aes_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(private_key_data)

        encrypted_private_key_path = f'{key_name}_encrypted_private_key.bin'
        with open(encrypted_private_key_path, 'wb') as encrypted_key_file:
            [encrypted_key_file.write(x) for x in (cipher_aes.nonce, tag, ciphertext)]

        QMessageBox.information(self, 'Private Key Encrypted', f'Private key encrypted with AES and saved as "{encrypted_private_key_path}".')
