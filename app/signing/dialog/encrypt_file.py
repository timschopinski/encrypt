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
        select_file_button.clicked.connect(self._select_file_to_encrypt)
        layout.addWidget(select_file_button)

        select_public_key_button = QPushButton('Select Public Key')
        select_public_key_button.clicked.connect(self._select_public_key)
        layout.addWidget(select_public_key_button)

        encrypt_button = QPushButton('Encrypt')
        encrypt_button.clicked.connect(self._validate_and_accept)
        layout.addWidget(encrypt_button)

        self._file_path = None
        self._public_key_path = None

    def extract_values(self):
        return {
            'file_path': self._file_path,
            'public_key_path': self._public_key_path,
        }

    def _select_file_to_encrypt(self):
        self._file_path = self._select_file('All Files (*)')
        if not self._file_path:
            self._show_error('File selected successfully.')

    def _select_public_key(self):
        self._public_key_path = self._select_file('Public Key Files (*.pem)')
        if not self._public_key_path:
            self._show_error('Public key selected successfully.')

    def _validate_and_accept(self):
        conditions = [
            (lambda: self._file_path, 'Please select a file to encrypt.'),
            (lambda: self._public_key_path, 'Please select a public key file.'),
            (lambda: os.path.exists(self._public_key_path), 'Public key not found.'),
            (lambda: os.path.exists(self._file_path), 'File Not Found')
        ]
        if self._validate(conditions):
            self.accept()
