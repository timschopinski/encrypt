from PyQt6.QtWidgets import QPushButton, QLineEdit, QLabel
from common.dialogs.base import BaseDialog
import os


class PrivateKeyEncryptionDialog(BaseDialog):
    def __init__(self):
        super().__init__('Encrypt Private Key')

        layout = self.layout()

        select_key_button = QPushButton('Select Key')
        select_key_button.clicked.connect(self._select_key)
        layout.addWidget(select_key_button)

        self._pin_input = QLineEdit()
        self._pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel('Enter PIN:'))
        layout.addWidget(self._pin_input)

        directory_button = QPushButton('Choose Directory')
        directory_button.clicked.connect(self._choose_directory)
        layout.addWidget(directory_button)

        encrypt_button = QPushButton('Encrypt')
        encrypt_button.clicked.connect(self._validate_and_accept)
        layout.addWidget(encrypt_button)

        self._key = None

    def extract_values(self):
        return {
            'key': self._key,
            'directory': self._directory,
            'pin': self._pin_input.text(),
        }

    def _select_key(self):
        self._key = self._select_file('Private Key (*.pem)')
        if not self._key:
            self._show_error('Please select a private key file.')

    def _validate_and_accept(self):
        conditions = [
            (lambda: self._key, 'Please select a private key file.'),
            (lambda: self._directory, 'Please select a directory.'),
            (lambda: self._pin_input.text(), 'Please enter a PIN.'),
            (lambda: os.path.exists(self._key), 'Private Key Not Found'),
            (lambda: os.path.exists(self._directory), 'Directory Not Found')
        ]
        if self._validate(conditions):
            self.accept()
