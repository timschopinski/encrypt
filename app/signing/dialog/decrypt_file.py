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
        select_file_button.clicked.connect(self.select_file_to_decrypt)
        layout.addWidget(select_file_button)

        select_private_key_button = QPushButton('Select Private Key')
        select_private_key_button.clicked.connect(self.select_private_key)
        layout.addWidget(select_private_key_button)

        decrypt_button = QPushButton('Decrypt')
        decrypt_button.clicked.connect(self.validate_and_accept)
        layout.addWidget(decrypt_button)

        self.file_path = None
        self.private_key_path = None

    def select_file_to_decrypt(self):
        self.file_path = self.select_file('All Files (*)')
        if not self.file_path:
            self.show_error('File selected successfully.')

    def select_private_key(self):
        self.private_key_path = self.select_file('Private Key Files (*.pem)')
        if not self.private_key_path:
            self.show_error('Public key selected successfully.')

    def validate_and_accept(self):
        conditions = [
            (lambda: self.file_path, 'Please select a file to decrypt.'),
            (lambda: self.private_key_path, 'Please select a private key file.'),
            (lambda: os.path.exists(self.private_key_path), 'Private key not found.'),
            (lambda: os.path.exists(self.file_path), 'File Not Found')
        ]
        if self.validate(conditions):
            self.accept()
