import os
import tempfile
import unittest
from PyQt6.QtWidgets import QApplication

from ttp.dialogs.key_config import KeyConfigDialog

app = QApplication([])


class TestKeyConfigDialog(unittest.TestCase):

    def test_dialog(self):
        dialog = KeyConfigDialog()

        dialog._algorithm_combo.setCurrentIndex(0)
        dialog._key_name_input.setText('test_key')
        dialog._bits_combo.setCurrentIndex(0)
        dialog._directory = tempfile.gettempdir()

        values = dialog.extract_values()
        expected_values = {
            'algorithm': 'RSA',
            'key': 'test_key',
            'bits': 1024,
            'directory': tempfile.gettempdir()
        }
        self.assertEqual(values, expected_values)
        dialog._validate_and_accept()
        self.assertTrue(dialog.result())

    def test_non_existing_directory(self):
        dialog = KeyConfigDialog()
        dialog._algorithm_combo.setCurrentIndex(0)
        dialog._key_name_input.setText('test_key')
        dialog._bits_combo.setCurrentIndex(0)
        dialog._directory = '/non_existing_directory'
        dialog._validate_and_accept()

        self.assertFalse(dialog.result())

    def test_missing_key_name(self):
        dialog = KeyConfigDialog()
        dialog._algorithm_combo.setCurrentIndex(0)
        dialog._bits_combo.setCurrentIndex(0)
        dialog._directory = tempfile.gettempdir()
        dialog._validate_and_accept()

        self.assertFalse(dialog.result())
