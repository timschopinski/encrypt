import os

from PyQt6.QtWidgets import QPushButton, QLabel, QLineEdit, QComboBox
from common.dialogs.base import BaseDialog
from common.backend.enums import Algorithm, RSABits, DSABits


class KeyConfigDialog(BaseDialog):
    def __init__(self):
        super().__init__('Key Generation Configuration')

        layout = self.layout()

        self._algorithm_combo = QComboBox()
        self._algorithm_combo.addItems([algorithm for algorithm in Algorithm])
        self._algorithm_combo.currentIndexChanged.connect(self._update_bits_combo)
        layout.addWidget(QLabel('Select algorithm:'))
        layout.addWidget(self._algorithm_combo)

        self._key_name_input = QLineEdit()
        layout.addWidget(QLabel('Enter name for keys (without extension):'))
        layout.addWidget(self._key_name_input)

        self._bits_combo = QComboBox()
        self._update_bits_combo()
        layout.addWidget(QLabel('Select number of bits for keys:'))
        layout.addWidget(self._bits_combo)

        directory_button = QPushButton('Choose Directory')
        directory_button.clicked.connect(self._choose_directory)
        layout.addWidget(directory_button)

        generate_button = QPushButton('Generate Keys')
        generate_button.clicked.connect(self._validate_and_accept)
        layout.addWidget(generate_button)

    def extract_values(self):
        return {
            'algorithm': self._algorithm_combo.currentText(),
            'key': self._key_name_input.text(),
            'bits': int(self._bits_combo.currentText()),
            'directory': self._directory,
        }

    def _update_bits_combo(self):
        self._bits_combo.clear()
        selected_algorithm = self._algorithm_combo.currentText()
        if selected_algorithm == Algorithm.RSA:
            self._bits_combo.addItems([str(bits.value) for bits in RSABits])
        elif selected_algorithm == Algorithm.DSA:
            self._bits_combo.addItems([str(bits.value) for bits in DSABits])
        else:
            self._bits_combo.addItems([str(bits.value) for bits in RSABits])

    def _validate_and_accept(self):
        conditions = [
            (lambda: self._directory, 'Please select a directory.'),
            (lambda: os.path.exists(self._directory), 'Directory Not Found'),
            (lambda: self._key_name_input.text(), 'Please enter a key name.')
        ]
        if self._validate(conditions):
            self.accept()
