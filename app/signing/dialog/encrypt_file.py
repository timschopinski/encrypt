from PyQt6.QtWidgets import QPushButton, QLineEdit, QLabel
from common.dialogs.base import BaseDialog
import os


class EncryptFileDialog(BaseDialog):
    def __init__(self):
        super().__init__('Encrypt File')

        layout = self.layout()

        self.label = QLabel('Please select the file to encrypt and the public key file.')
        layout.addWidget(self.label)

        select_file_button = QPushButton('Select File')
        select_file_button.clicked.connect(self.select_file_to_encrypt)
        layout.addWidget(select_file_button)

        select_public_key_button = QPushButton('Select Public Key')
        select_public_key_button.clicked.connect(self.select_public_key)
        layout.addWidget(select_public_key_button)

        encrypt_button = QPushButton('Encrypt')
        encrypt_button.clicked.connect(self.validate_and_accept)
        layout.addWidget(encrypt_button)

        self.file_path = None
        self.public_key_path = None

    def select_file_to_encrypt(self):
        self.file_path = self.select_file('All Files (*)')
        if not self.file_path:
            self.show_error('File selected successfully.')

    def select_public_key(self):
        self.public_key_path = self.select_file('Public Key Files (*.pem)')
        if not self.public_key_path:
            self.show_error('Public key selected successfully.')

    def validate_and_accept(self):
        conditions = [
            (lambda: self.file_path, 'Please select a file to encrypt.'),
            (lambda: self.public_key_path, 'Please select a public key file.'),
            (lambda: os.path.exists(self.public_key_path), 'Public key not found.'),
            (lambda: os.path.exists(self.file_path), 'File Not Found')
        ]
        if self.validate(conditions):
            self.accept()
