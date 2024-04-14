from PyQt6.QtWidgets import QPushButton, QMessageBox, QDialog

from ttp.backend.encryption import PrivateKeyEncryptor
from ttp.backend.factories import GenericKeyFactory

from common.windows.base import BaseWindow
from ttp.dialogs.key_encryption import PrivateKeyEncryptionDialog
from ttp.dialogs.key_config import KeyConfigDialog


class TTPWindow(BaseWindow):
    window_title = 'TTP Application'

    def initUI(self):
        super().initUI()

        generate_keys_button = QPushButton('Generate Asymmetric Keys', self)
        generate_keys_button.clicked.connect(self.show_key_config_dialog)
        self.layout.addWidget(generate_keys_button)

        encrypt_key_button = QPushButton('Encrypt Private Key', self)
        encrypt_key_button.clicked.connect(self.show_encrypt_private_key_dialog)
        self.layout.addWidget(encrypt_key_button)

    def show_key_config_dialog(self):
        dialog = KeyConfigDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            GenericKeyFactory.create(dialog.algorithm, dialog.key, dialog.bits, dialog.directory)
            QMessageBox.information(self, 'Success', f'{dialog.algorithm} Keys Generated.')

    def show_encrypt_private_key_dialog(self):
        dialog = PrivateKeyEncryptionDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            PrivateKeyEncryptor.encrypt(dialog.key, dialog.directory, dialog.pin)
            QMessageBox.information(self, 'Success', 'Private Key Encrypted')
