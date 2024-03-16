from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QRect, QCoreApplication


class BaseWindow(QWidget):
    window_title = 'App'

    def __init__(self):
        super().__init__()
        self.status_label = None
        self.initUI()

    def initUI(self):
        screen_geometry = QCoreApplication.instance().primaryScreen().geometry()
        widget_geometry = QRect(screen_geometry.width() // 2 - 200, screen_geometry.height() // 2 - 150, 400, 300)

        self.setWindowTitle(self.window_title)
        self.setGeometry(widget_geometry)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.status_label = QLabel(self)
        self.layout.addWidget(self.status_label)

    def display_status(self, message):
        self.status_label.setText(message)
