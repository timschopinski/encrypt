from PyQt6.QtWidgets import QPushButton, QFileDialog, QMessageBox, QLabel, QDialog
from signing.backend.handlers import EncryptFileHandler, DecryptFileHandler
from signing.backend.signing import DocumentSigner
from common.windows.base import BaseWindow
from signing.dialog.decrypt_file import DecryptFileDialog
from signing.dialog.encrypt_file import EncryptFileDialog


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
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Document to Sign', '', 'All Files (*)')
        if file_path:
            document_signer = DocumentSigner('/path/to/user_A_private_key.pem')

            signature = document_signer.sign_document(file_path)
            signature_file_path = file_path + '.xml'
            with open(signature_file_path, 'wb') as signature_file:
                signature_file.write(signature)

            QMessageBox.information(self, 'Signature Created', f'Signature saved to {signature_file_path}')

    def encrypt_file(self):
        dialog = EncryptFileDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            if EncryptFileHandler.encrypt_file(dialog.file_path, dialog.public_key_path):
                self.display_status(f'Encryption Complete')
            else:
                self.display_status('Encryption failed.')

    def decrypt_file(self):
        dialog = DecryptFileDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            if DecryptFileHandler.decrypt_file(dialog.file_path, dialog.private_key_path):
                self.display_status(f'Decryption Completed Successfully.')
            else:
                self.display_status('Decryption failed.')
