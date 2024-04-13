from PyQt6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QLabel, QLineEdit, QComboBox, QFileDialog
from crypto.enums import Algorithm, RSABits, DSABits


class KeyConfigDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Key Generation Configuration')

        layout = QVBoxLayout()

        self.error_label = QLabel()
        layout.addWidget(self.error_label)

        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItems([algorithm for algorithm in Algorithm])
        self.algorithm_combo.currentIndexChanged.connect(self.update_bits_combo)
        layout.addWidget(QLabel('Select algorithm:'))
        layout.addWidget(self.algorithm_combo)

        self.key_name_input = QLineEdit()
        layout.addWidget(QLabel('Enter name for keys (without extension):'))
        layout.addWidget(self.key_name_input)

        self.bits_combo = QComboBox()
        self.update_bits_combo()
        layout.addWidget(QLabel('Select number of bits for keys:'))
        layout.addWidget(self.bits_combo)

        self.directory_button = QPushButton('Choose Directory')
        self.directory_button.clicked.connect(self.choose_directory)
        layout.addWidget(self.directory_button)

        self.generate_button = QPushButton('Generate Keys')
        self.generate_button.clicked.connect(self.validate)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

        self.key = None
        self.bits = None
        self.algorithm = None
        self.directory = None

    def extract_values(self):
        self.bits = int(self.bits_combo.currentText())
        self.algorithm = self.algorithm_combo.currentText()
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

        self.extract_values()
        self.accept()

    def update_bits_combo(self):
        self.bits_combo.clear()
        selected_algorithm = self.algorithm_combo.currentText()
        if selected_algorithm == Algorithm.RSA:
            self.bits_combo.addItems([str(bits.value) for bits in RSABits])
        elif selected_algorithm == Algorithm.DSA:
            self.bits_combo.addItems([str(bits.value) for bits in DSABits])
        else:
            self.bits_combo.addItems([str(bits.value) for bits in RSABits])
