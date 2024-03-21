from PyQt6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QLabel, QLineEdit, QComboBox, QFileDialog
from crypto.enums import RSAKeyBits


class RSAConfigDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('RSA Key Generation Configuration')

        layout = QVBoxLayout()

        self.error_label = QLabel()
        layout.addWidget(self.error_label)

        self.key_name_input = QLineEdit()
        layout.addWidget(QLabel('Enter name for RSA keys (without extension):'))
        layout.addWidget(self.key_name_input)

        self.bits_combo = QComboBox()
        self.bits_combo.addItems([str(bits.value) for bits in RSAKeyBits])
        layout.addWidget(QLabel('Select number of bits for RSA keys:'))
        layout.addWidget(self.bits_combo)

        self.directory_button = QPushButton('Choose Directory')
        self.directory_button.clicked.connect(self.choose_directory)
        layout.addWidget(self.directory_button)

        self.generate_button = QPushButton('Generate RSA Keys')
        self.generate_button.clicked.connect(self.validate)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

        self.key = None
        self.bits = None
        self.directory = None

    def post_validation(self):
        self.bits = int(self.bits_combo.currentText())
        self.key = self.key_name_input.text()

    def choose_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Choose Directory')
        if directory:
            self.directory = directory

    def validate(self):
        if not self.directory:
            self.error_label.setText('Please select a directory.')
            return

        if not self.key_name_input.text():
            self.error_label.setText('Please enter a key name.')
            return

        self.post_validation()
        self.accept()
