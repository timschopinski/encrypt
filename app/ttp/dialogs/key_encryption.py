from PyQt6.QtWidgets import QPushButton, QLineEdit, QLabel
from common.dialogs.base import BaseDialog
import os


class PrivateKeyEncryptionDialog(BaseDialog):
    def __init__(self):
        super().__init__('Encrypt Private Key')

        layout = self.layout()

        self.select_key_button = QPushButton('Select Key')
        self.select_key_button.clicked.connect(self.select_key)
        layout.addWidget(self.select_key_button)

        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel('Enter PIN:'))
        layout.addWidget(self.pin_input)

        self.directory_button = QPushButton('Choose Directory')
        self.directory_button.clicked.connect(self.choose_directory)
        layout.addWidget(self.directory_button)

        encrypt_button = QPushButton('Encrypt')
        encrypt_button.clicked.connect(self.validate_and_accept)
        layout.addWidget(encrypt_button)

        self.key = None
        self.pin = None
        self.directory = None

    def select_key(self):
        self.key = self.select_file('Private Key (*.pem)')
        if not self.key:
            self.show_error('Please select a private key file.')

    def extract_values(self):
        self.pin = self.pin_input.text()

    def validate_and_accept(self):
        conditions = [
            (lambda: self.key, 'Please select a private key file.'),
            (lambda: self.directory, 'Please select a directory.'),
            (lambda: self.pin_input.text(), 'Please enter a PIN.'),
            (lambda: os.path.exists(self.key), 'Private Key Not Found')
        ]
        if self.validate(conditions):
            self.extract_values()
            self.accept()
