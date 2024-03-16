from PyQt6.QtWidgets import QWidget, QPushButton, QFileDialog, QMessageBox, QLineEdit, QLabel, QVBoxLayout

from crypto.rsa import RSAKeys
from crypto.signing import DocumentSigner
import os
from Crypto.Cipher import AES
from hashlib import sha256


class SignatureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Signature Tool')
        self.setGeometry(100, 100, 400, 300)

        self.sign_button = QPushButton('Sign Document', self)
        self.sign_button.clicked.connect(self.sign_document)
        self.sign_button.setGeometry(50, 50, 150, 30)

        self.encrypt_button = QPushButton('Encrypt File', self)
        self.encrypt_button.clicked.connect(self.encrypt_file)
        self.encrypt_button.setGeometry(50, 100, 150, 30)

        self.decrypt_button = QPushButton('Decrypt File', self)
        self.decrypt_button.clicked.connect(self.decrypt_file)
        self.decrypt_button.setGeometry(50, 150, 150, 30)

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
            # TODO: Implement encryption logic here
            pass

    def decrypt_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select File to Decrypt', '', 'All Files (*)')
        if file_path:
            # TODO: Implement decryption logic here
            pass


class TTPApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TTP Application')
        self.setGeometry(100, 100, 400, 300)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.key_name_input = QLineEdit(self)
        self.layout.addWidget(QLabel('Enter name for RSA keys (without extension):'))
        self.layout.addWidget(self.key_name_input)

        self.generate_keys_button = QPushButton('Generate RSA Keys', self)
        self.generate_keys_button.clicked.connect(self.generate_rsa_keys)
        self.layout.addWidget(self.generate_keys_button)

        self.encrypt_key_button = QPushButton('Encrypt Private Key', self)
        self.encrypt_key_button.clicked.connect(self.encrypt_private_key)
        self.layout.addWidget(self.encrypt_key_button)

        self.pin_input = QLineEdit(self)
        self.layout.addWidget(QLabel('Enter User A PIN:'))
        self.layout.addWidget(self.pin_input)

        self.setLayout(self.layout)

    def generate_rsa_keys(self):
        key_name = self.key_name_input.text()
        if not key_name:
            QMessageBox.warning(self, 'Empty Key Name', 'Please enter a name for the RSA keys.')
            return

        rsa_keys = RSAKeys()
        rsa_keys.create(key_name)
        QMessageBox.information(self, 'Success', 'RSA Keys Generated.')

    def encrypt_private_key(self):
        pin = self.pin_input.text()
        if not pin:
            QMessageBox.warning(self, 'Empty PIN', 'Please enter a PIN.')
            return

        key_name = self.key_name_input.text()
        if not key_name:
            QMessageBox.warning(self, 'Empty Key Name', 'Please enter a name for the RSA keys.')
            return

        private_key_path = f'{key_name}_private_key.pem'
        if not os.path.exists(private_key_path):
            QMessageBox.warning(self, 'Private Key Not Found', 'Private key not found. Generate RSA keys first.')
            return

        with open(private_key_path, 'rb') as private_key_file:
            private_key_data = private_key_file.read()

        aes_key = sha256(pin.encode()).digest()

        cipher_aes = AES.new(aes_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(private_key_data)

        encrypted_private_key_path = f'{key_name}_encrypted_private_key.bin'
        with open(encrypted_private_key_path, 'wb') as encrypted_key_file:
            [encrypted_key_file.write(x) for x in (cipher_aes.nonce, tag, ciphertext)]

        QMessageBox.information(self, 'Private Key Encrypted', f'Private key encrypted with AES and saved as "{encrypted_private_key_path}".')
