import os
import tempfile
import unittest
from PyQt6.QtWidgets import QApplication

from ttp.dialogs.key_encryption import PrivateKeyEncryptionDialog

app = QApplication([])


class TestPrivateKeyEncryptionDialog(unittest.TestCase):
    def test_dialog(self):
        dialog = PrivateKeyEncryptionDialog()
        temp_key_file = os.path.join(tempfile.gettempdir(), 'test_key.pem')
        with open(temp_key_file, 'w') as f:
            f.write("Temporary key file content")

        dialog._key = temp_key_file
        dialog._pin_input.setText('1234')
        dialog._directory = tempfile.gettempdir()

        values = dialog.extract_values()
        expected_values = {
            'key': os.path.join(tempfile.gettempdir(), 'test_key.pem'),
            'directory': tempfile.gettempdir(),
            'pin': '1234',
        }
        self.assertEqual(values, expected_values)
        dialog._validate_and_accept()
        self.assertTrue(dialog.result())

    def test_missing_key(self):
        dialog = PrivateKeyEncryptionDialog()
        dialog._pin_input.setText('1234')
        dialog._directory = tempfile.gettempdir()
        dialog._validate_and_accept()

        self.assertFalse(dialog.result())

    def test_missing_directory(self):
        dialog = PrivateKeyEncryptionDialog()
        dialog._key = os.path.join(tempfile.gettempdir(), 'test_key.pem')
        dialog._pin_input.setText('1234')
        dialog._validate_and_accept()

        self.assertFalse(dialog.result())

    def test_missing_pin(self):
        dialog = PrivateKeyEncryptionDialog()
        dialog._key = os.path.join(tempfile.gettempdir(), 'test_key.pem')
        dialog._directory = tempfile.gettempdir()
        dialog._validate_and_accept()

        self.assertFalse(dialog.result())

    def test_non_existing_key(self):
        dialog = PrivateKeyEncryptionDialog()
        dialog._key = '/non_existing_key.pem'
        dialog._pin_input.setText('1234')
        dialog._directory = tempfile.gettempdir()
        dialog._validate_and_accept()

        self.assertFalse(dialog.result())
