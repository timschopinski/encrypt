from PyQt6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QLabel, QLineEdit, QComboBox, QFileDialog
from crypto.enums import RSAKeyBits


class RSAConfigDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('RSA Key Generation Configuration')

        self.layout = QVBoxLayout()

        self.key_name_input = QLineEdit()
        self.layout.addWidget(QLabel('Enter name for RSA keys (without extension):'))
        self.layout.addWidget(self.key_name_input)

        self.bits_combo = QComboBox()
        self.bits_combo.addItems([str(bits.value) for bits in RSAKeyBits])
        self.layout.addWidget(QLabel('Select number of bits for RSA keys:'))
        self.layout.addWidget(self.bits_combo)

        self.directory_button = QPushButton('Choose Directory')
        self.directory_button.clicked.connect(self.choose_directory)
        self.layout.addWidget(self.directory_button)

        self.generate_button = QPushButton('Generate RSA Keys')
        self.generate_button.clicked.connect(self.accept)
        self.layout.addWidget(self.generate_button)

        self.setLayout(self.layout)

    def choose_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Choose Directory')
        if directory:
            self.directory = directory
