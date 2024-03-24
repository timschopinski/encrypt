from PyQt6.QtWidgets import QPushButton, QMessageBox, QDialog
from crypto.factories import RSAKeyFactory
import os
from Crypto.Cipher import AES
from hashlib import sha256
from gui.base import BaseWindow
from gui.dialogs.key_encryption import PrivateKeyEncryptionDialog
from gui.dialogs.rsa_config import RSAConfigDialog


class TTPWindow(BaseWindow):
    window_title = 'TTP Application'

    def initUI(self):
        super().initUI()

        generate_keys_button = QPushButton('Generate RSA Keys', self)
        generate_keys_button.clicked.connect(self.show_rsa_config_dialog)
        self.layout.addWidget(generate_keys_button)

        encrypt_key_button = QPushButton('Encrypt Private Key', self)
        encrypt_key_button.clicked.connect(self.show_encrypt_private_key_dialog)
        self.layout.addWidget(encrypt_key_button)

    def show_rsa_config_dialog(self):
        dialog = RSAConfigDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            rsa_keys = RSAKeyFactory()
            rsa_keys.create(dialog.key, dialog.bits, dialog.directory)
            QMessageBox.information(self, 'Success', 'RSA Keys Generated.')

    def show_encrypt_private_key_dialog(self):
        dialog = PrivateKeyEncryptionDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.encrypt_private_key(dialog.key, dialog.directory, dialog.pin)

    def encrypt_private_key(self, key: str, directory: str, pin: str):
        with open(key, 'rb') as private_key_file:
            private_key_data = private_key_file.read()

        aes_key = sha256(pin.encode()).digest()

        cipher_aes = AES.new(aes_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(private_key_data)
        key_without_extension = os.path.splitext(os.path.basename(key))[0].replace('_private_key', '')
        encrypted_private_key_path = f'{key_without_extension}_encrypted_private_key.bin'
        with open(os.path.join(directory, encrypted_private_key_path), 'wb') as encrypted_key_file:
            [encrypted_key_file.write(x) for x in (cipher_aes.nonce, tag, ciphertext)]

        QMessageBox.information(self, 'Private Key Encrypted', f'Private key encrypted with AES and saved as "{encrypted_private_key_path}".')
