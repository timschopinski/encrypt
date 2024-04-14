import os
from PyQt6.QtWidgets import QPushButton, QLineEdit, QLabel
from common.dialogs.base import BaseDialog


class SignDocumentDialog(BaseDialog):
    def __init__(self):
        super().__init__('Sign Document')

        layout = self.layout()

        select_file_button = QPushButton('Select File')
        select_file_button.clicked.connect(self._select_file_to_sign)
        layout.addWidget(select_file_button)

        select_encrypted_private_key_button = QPushButton('Select Encrypted Private Key')
        select_encrypted_private_key_button.clicked.connect(self._select_encrypted_private_key_path)
        layout.addWidget(select_encrypted_private_key_button)

        self._user_input = QLineEdit()
        layout.addWidget(QLabel('Enter user information (username):'))
        layout.addWidget(self._user_input)

        self._pin_input = QLineEdit()
        self._pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel('Enter PIN:'))
        layout.addWidget(self._pin_input)

        sign_button = QPushButton('Sign')
        sign_button.clicked.connect(self._validate_and_accept)
        layout.addWidget(sign_button)

        self._file_path = None
        self._encrypted_private_key_path = None

    def extract_values(self):
        return {
            'file_path': self._file_path,
            'encrypted_private_key_path': self._encrypted_private_key_path,
            'pin': self._pin_input.text(),
            'user': self._user_input.text(),
        }

    def _select_file_to_sign(self):
        self._file_path = self._select_file('All Files (*)')
        if not self._file_path:
            self._show_error('Please select a file to sign.')

    def _select_encrypted_private_key_path(self):
        self._encrypted_private_key_path = self._select_file('Private Key Files (*.pem)')
        if not self._encrypted_private_key_path:
            self._show_error('Please select a encrypted private key file.')

    def _validate_and_accept(self):
        conditions = [
            (lambda: self._file_path, 'Please select a file to encrypt.'),
            (lambda: self._encrypted_private_key_path, 'Please select a encrypted private key file.'),
            (lambda: os.path.exists(self._encrypted_private_key_path), 'Encrypted Private key not found.'),
            (lambda: os.path.exists(self._file_path), 'File Not Found'),
            (lambda: self._pin_input.text(), 'Please enter a PIN.'),
            (lambda: self._user_input.text(), 'Please enter a user information.')
        ]
        if self._validate(conditions):
            self.accept()
