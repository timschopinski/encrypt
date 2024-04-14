from PyQt6.QtWidgets import QPushButton, QFileDialog, QMessageBox, QLabel, QDialog
from signing.backend.handlers import EncryptFileHandler, DecryptFileHandler
from signing.backend.signing import DocumentSigner
from common.windows.base import BaseWindow
from signing.dialog.decrypt_file import DecryptFileDialog
from signing.dialog.encrypt_file import EncryptFileDialog
from signing.dialog.sign_document import SignDocumentDialog


class SigningWindow(BaseWindow):
    window_title = 'Signature Tool'

    def initUI(self):
        super().initUI()

        sign_button = QPushButton('Sign Document', self)
        sign_button.clicked.connect(self.sign_document)
        self.layout.addWidget(sign_button)

        encrypt_button = QPushButton('Encrypt File', self)
        encrypt_button.clicked.connect(self.encrypt_file)
        self.layout.addWidget(encrypt_button)

        decrypt_button = QPushButton('Decrypt File', self)
        decrypt_button.clicked.connect(self.decrypt_file)
        self.layout.addWidget(decrypt_button)

        self.status_label = QLabel(self)
        self.layout.addWidget(self.status_label)

    def sign_document(self):
        dialog = SignDocumentDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            file_path, encrypted_private_key_path, pin, username = dialog.extract_values().values()
            document_signer = DocumentSigner(encrypted_private_key_path)

            _, created = document_signer.sign_document(file_path, pin, username)
            if created:
                self.display_status(f'Signature Completed Successfully.')
            else:
                self.display_status('Signature failed.')


    def encrypt_file(self):
        dialog = EncryptFileDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            file_path, public_key_path = dialog.extract_values().values()
            if EncryptFileHandler.encrypt_file(file_path, public_key_path):
                self.display_status(f'Encryption Completed Successfully.')
            else:
                self.display_status('Encryption failed.')

    def decrypt_file(self):
        dialog = DecryptFileDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            file_path, private_key_path = dialog.extract_values().values()
            if DecryptFileHandler.decrypt_file(file_path, private_key_path):
                self.display_status(f'Decryption Completed Successfully.')
            else:
                self.display_status('Decryption failed.')
