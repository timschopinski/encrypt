from PyQt6.QtWidgets import QPushButton

from common.windows.base import BaseWindow
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

    def open_signing_app(self):
        self.signing_app = SigningWindow()
        self.signing_app.show()

    def open_ttp_app(self):
        self.ttp = TTPWindow()
        self.ttp.show()
