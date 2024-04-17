from typing import Any

from PyQt6.QtCore import QCoreApplication, QRect
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QFileDialog


class BaseDialog(QDialog):
    validators = None

    def __init__(self, title):
        super().__init__()
        screen_geometry = QCoreApplication.instance().primaryScreen().geometry()
        widget_geometry = QRect(screen_geometry.width() // 2 - 200, screen_geometry.height() // 2 - 150, 400, 300)

        self.setWindowTitle(title)
        self.setGeometry(widget_geometry)

        layout = QVBoxLayout()

        self.error_label = QLabel()
        layout.addWidget(self.error_label)

        self.setLayout(layout)
        self._directory = None

    def extract_values(self) -> dict[str, Any]:
        pass

    def _choose_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Choose Directory')
        if directory:
            self._directory = directory

    def _select_file(self, name_filter):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter(name_filter)
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                return selected_files[0]

    def _show_error(self, message):
        self.error_label.setText(message)
        self.error_label.setStyleSheet('color: red;')

    def _validate(self, conditions):
        for condition, error_message in conditions:
            if not condition():
                self._show_error(error_message)
                return False
        return True
