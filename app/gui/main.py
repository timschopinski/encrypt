from PyQt6.QtWidgets import QPushButton

from gui.base import BaseWindow
from gui.app import AppWindow
from gui.ttp import TTPWindow


class MainWindow(BaseWindow):
    window_title = 'Encrypt'

    def initUI(self):
        super().initUI()

        signature_button = QPushButton('Open Signature App', self)
        signature_button.clicked.connect(self.open_main_app())
        self.layout.addWidget(signature_button)

        ttp_button = QPushButton('Open TTP App', self)
        ttp_button.clicked.connect(self.open_ttp_app)
        self.layout.addWidget(ttp_button)

    @staticmethod
    def open_main_app():
        app = AppWindow()
        app.show()

    @staticmethod
    def open_ttp_app():
        ttp = TTPWindow()
        ttp.show()
