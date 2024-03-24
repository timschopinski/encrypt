from PyQt6.QtWidgets import QPushButton, QFileDialog, QMessageBox, QLabel

from crypto.algorithms import RsaAlgorithm
from crypto.signing import DocumentSigner
from Crypto.Cipher import PKCS1_OAEP
from gui.base import BaseWindow


class SignatureWindow(BaseWindow):
    window_title = 'Signature Tool'

    def initUI(self):
        super().initUI()

        self.sign_button = QPushButton('Sign Document', self)
        self.sign_button.clicked.connect(self.sign_document)
        self.layout.addWidget(self.sign_button)

        self.encrypt_button = QPushButton('Encrypt File', self)
        self.encrypt_button.clicked.connect(self.encrypt_file)
        self.layout.addWidget(self.encrypt_button)

        self.decrypt_button = QPushButton('Decrypt File', self)
        self.decrypt_button.clicked.connect(self.decrypt_file)
        self.layout.addWidget(self.decrypt_button)

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
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select File to Encrypt', '', 'All Files (*)')
        if file_path:
            QMessageBox.information(self, 'Select Public Key', 'Please select the public key for encryption.')
            public_key_path, _ = QFileDialog.getOpenFileName(self, 'Select Public Key', '', 'Public Key Files (*.pem)')
            if not public_key_path:
                self.display_status('Encryption canceled.')
                return

            public_key = RsaAlgorithm.load_key(public_key_path)

            with open(file_path, 'rb') as f:
                plaintext = f.read()

            cipher_rsa = PKCS1_OAEP.new(public_key)
            ciphertext = cipher_rsa.encrypt(plaintext)

            encrypted_file_path, _ = QFileDialog.getSaveFileName(self, 'Save Encrypted File', '', 'All Files (*)')
            if encrypted_file_path:
                with open(encrypted_file_path, 'wb') as f:
                    f.write(ciphertext)
                self.display_status(f'Encryption Complete')

    def decrypt_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select File to Decrypt', '', 'All Files (*)')
        if file_path:
            QMessageBox.information(self, 'Select Private Key', 'Please select the private key for decryption.')

            private_key_path, _ = QFileDialog.getOpenFileName(self, 'Select Private Key', '', 'Private Key Files (*.pem)')
            if not private_key_path:
                self.display_status('Decryption canceled.')
                return

            private_key = RsaAlgorithm.load_key(private_key_path)

            with open(file_path, 'rb') as f:
                ciphertext = f.read()

            cipher_rsa = PKCS1_OAEP.new(private_key)
            plaintext = cipher_rsa.decrypt(ciphertext)

            decrypted_file_path, _ = QFileDialog.getSaveFileName(self, 'Save Decrypted File', '', 'All Files (*)')
            if decrypted_file_path:
                with open(decrypted_file_path, 'wb') as f:
                    f.write(plaintext)
                self.display_status(f'Decryption Completed Successfully.')
