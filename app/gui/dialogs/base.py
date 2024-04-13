import os
from PyQt6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QLabel, QLineEdit, QFileDialog


class BaseDialog(QDialog):
    def __init__(self, title):
        super().__init__()

        self.setWindowTitle(title)

        layout = QVBoxLayout()

        self.error_label = QLabel()
        layout.addWidget(self.error_label)

        self.setLayout(layout)

    def choose_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Choose Directory')
        if directory:
            self.directory = directory

    def select_file(self, name_filter):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter(name_filter)
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                return selected_files[0]

    def show_error(self, message):
        self.error_label.setText(message)
        self.error_label.setStyleSheet('color: red;')

    def validate(self, conditions):
        for condition, error_message in conditions:
            if not condition():
                self.show_error(error_message)
                return False
        return True
