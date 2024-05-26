from PyQt6.QtWidgets import QPushButton

from common.windows.base import BaseWindow
from password_manager.main import PasswordManagerWindow
from signing.main import SigningWindow
from ttp.main import TTPWindow


class MainWindow(BaseWindow):
    window_title = 'Encrypt'

    def initUI(self):
        super().initUI()

        signing_button = QPushButton('Open Signing App', self)
        signing_button.clicked.connect(self.open_signing_app)
        self.layout.addWidget(signing_button)

        ttp_button = QPushButton('Open TTP App', self)
        ttp_button.clicked.connect(self.open_ttp_app)
        self.layout.addWidget(ttp_button)

        password_manager_button = QPushButton('Password Manager', self)
        password_manager_button.clicked.connect(self.open_password_manager)
        self.layout.addWidget(password_manager_button)

    def open_signing_app(self):
        self.signing_app = SigningWindow()
        self.signing_app.show()

    def open_ttp_app(self):
        self.ttp = TTPWindow()
        self.ttp.show()

    def open_password_manager(self):
        self.password_manager = PasswordManagerWindow()
        self.password_manager.show()
