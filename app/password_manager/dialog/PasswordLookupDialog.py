import os
from PyQt6.QtWidgets import QPushButton, QLineEdit, QLabel, QMessageBox
from common.dialogs.base import BaseDialog
from signing.backend.pendrive_search import PendriveSearchThread


class PasswordLookupDialog(BaseDialog):
    def __init__(self):
        super().__init__('Password Lookup')

        layout = self.layout()

        select_file_button = QPushButton('Select File')
        select_file_button.clicked.connect(self._select_file_to_lookup)
        layout.addWidget(select_file_button)

        select_encrypted_private_key_button = QPushButton('Select Encrypted Private Key')
        select_encrypted_private_key_button.clicked.connect(self._select_encrypted_private_key_path)
        layout.addWidget(select_encrypted_private_key_button)

        self._pin_input = QLineEdit()
        self._pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel('Enter PIN:'))
        layout.addWidget(self._pin_input)

        lookup_button = QPushButton('Lookup')
        lookup_button.clicked.connect(self._validate_and_accept)
        layout.addWidget(lookup_button)

        self._file_path = None
        self._encrypted_private_key_path = None

        self.pendrive_search_thread = PendriveSearchThread(is_encrypted=True)
        self.pendrive_search_thread.worker.found_private_key.connect(self._handle_found_private_key)
        self.pendrive_search_thread.finished.connect(self.pendrive_search_thread.deleteLater)
        self.pendrive_search_thread.start()

    def extract_values(self):
        return {
            'file_path': self._file_path,
            'encrypted_private_key_path': self._encrypted_private_key_path,
            'pin': self._pin_input.text(),
        }

    def closeEvent(self, event):
        self.pendrive_search_thread.worker.stop_search()
        self.pendrive_search_thread.quit()
        self.pendrive_search_thread.wait()
        event.accept()

    def _handle_found_private_key(self, encrypted_private_key_path):
        QMessageBox.information(self, 'Success', f'Automatically detected {encrypted_private_key_path}.')
        self._encrypted_private_key_path = encrypted_private_key_path

    def _select_file_to_lookup(self):
        self._file_path = self._select_file('All Files (*)')
        if not self._file_path:
            self._show_error('Please select a file to lookup.')

    def _select_encrypted_private_key_path(self):
        self._encrypted_private_key_path = self._select_file('Private Key Files (*.pem)')
        if not self._encrypted_private_key_path:
            self._show_error('Please select an encrypted private key file.')

    def _validate_and_accept(self):
        conditions = [
            (lambda: self._file_path, 'Please select a file to encrypt.'),
            (lambda: self._encrypted_private_key_path, 'Please select an encrypted private key file.'),
            (lambda: os.path.exists(self._encrypted_private_key_path), 'Encrypted Private key not found.'),
            (lambda: os.path.exists(self._file_path), 'File Not Found'),
            (lambda: self._pin_input.text(), 'Please enter a PIN.'),
        ]
        if self._validate(conditions):
            self.accept()
