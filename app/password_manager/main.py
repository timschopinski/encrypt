from PyQt6.QtWidgets import QPushButton, QLabel, QDialog, QMessageBox
from common.backend.exceptions import EncryptException
from password_manager.backend.password_manager import PasswordManager
from password_manager.dialog.PasswordLookupDialog import PasswordLookupDialog
from common.windows.base import BaseWindow


class PasswordManagerWindow(BaseWindow):
    window_title = 'Password Manager'

    def initUI(self):
        super().initUI()

        password_lookup_button = QPushButton('Password lookup', self)
        password_lookup_button.clicked.connect(self.password_lookup)
        self.layout.addWidget(password_lookup_button)

        self.status_label = QLabel(self)
        self.layout.addWidget(self.status_label)

    def password_lookup(self):
        self.clear_status()
        dialog = PasswordLookupDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            file_path, encrypted_private_key_path, pin = dialog.extract_values().values()
            password_manager = PasswordManager(encrypted_private_key_path)
            try:
                content = password_manager.lookup(file_path, pin)
                QMessageBox.information(self, 'Success', content)
            except EncryptException as e:
                self.display_status(e.message)
