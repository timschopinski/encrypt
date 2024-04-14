from PyQt6.QtWidgets import QPushButton, QLineEdit, QLabel
from common.dialogs.base import BaseDialog
import os


class DecryptFileDialog(BaseDialog):
    def __init__(self):
        super().__init__('Decrypt File')

        layout = self.layout()

        self.label = QLabel('Please select the file to decrypt and the private key file.')
        layout.addWidget(self.label)

        select_file_button = QPushButton('Select File')
        select_file_button.clicked.connect(self._select_file_to_decrypt)
        layout.addWidget(select_file_button)

        select_private_key_button = QPushButton('Select Private Key')
        select_private_key_button.clicked.connect(self._select_private_key)
        layout.addWidget(select_private_key_button)

        decrypt_button = QPushButton('Decrypt')
        decrypt_button.clicked.connect(self._validate_and_accept)
        layout.addWidget(decrypt_button)

        self._file_path = None
        self._private_key_path = None

    def extract_values(self):
        return {
            'file_path': self._file_path,
            'private_key_path': self._private_key_path,
        }

    def _select_file_to_decrypt(self):
        self._file_path = self._select_file('All Files (*)')
        if not self._file_path:
            self._show_error('File selected successfully.')

    def _select_private_key(self):
        self._private_key_path = self._select_file('Private Key Files (*.pem)')
        if not self._private_key_path:
            self._show_error('Public key selected successfully.')

    def _validate_and_accept(self):
        conditions = [
            (lambda: self._file_path, 'Please select a file to decrypt.'),
            (lambda: self._private_key_path, 'Please select a private key file.'),
            (lambda: os.path.exists(self._private_key_path), 'Private key not found.'),
            (lambda: os.path.exists(self._file_path), 'File Not Found')
        ]
        if self._validate(conditions):
            self.accept()
