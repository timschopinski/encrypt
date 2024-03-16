from PyQt6.QtWidgets import QPushButton

from gui.base import BaseWindow
from gui.signature import SignatureWindow
from gui.ttp import TTPWindow


class MainWindow(BaseWindow):
    window_title = 'Encrypt'

    def initUI(self):
        super().initUI()

        signature_button = QPushButton('Open Signature App', self)
        signature_button.clicked.connect(self.open_signature_app)
        self.layout.addWidget(signature_button)

        ttp_button = QPushButton('Open TTP App', self)
        ttp_button.clicked.connect(self.open_ttp_app)
        self.layout.addWidget(ttp_button)

    def open_signature_app(self):
        self.signature = SignatureWindow()
        self.signature.show()

    def open_ttp_app(self):
        self.ttp = TTPWindow()
        self.ttp.show()
