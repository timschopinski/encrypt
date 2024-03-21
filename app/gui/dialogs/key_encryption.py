import os

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox


class PrivateKeyEncryptionDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Encrypt Private Key')

        layout = QVBoxLayout()

        self.error_label = QLabel()
        layout.addWidget(self.error_label)

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
        encrypt_button.clicked.connect(self.validate)
        layout.addWidget(encrypt_button)

        self.setLayout(layout)

        self.key = None
        self.pin = None
        self.directory = None

    def choose_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Choose Directory')
        if directory:
            self.directory = directory

    def select_key(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter('RSA Private Key (*.pem)')
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.key = selected_files[0]

    def post_validate(self):
        self.pin = self.pin_input.text()

    def validate(self):
        if not self.key:
            self.error_label.setText('Please select a private key file.')
            return
        if not self.directory:
            self.error_label.setText('Please select a directory.')
            return
        if not self.pin_input.text():
            self.error_label.setText('Please enter a PIN.')
            return
        if not os.path.exists(self.key):
            self.error_label.setText('Private Key Not Found')
            return

        self.post_validate()
        self.accept()
