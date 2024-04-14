from PyQt6.QtWidgets import QPushButton, QFileDialog, QLabel, QVBoxLayout, QLineEdit
from common.dialogs.base import BaseDialog
import os


class ValidateSignatureDialog(BaseDialog):
    def __init__(self):
        super().__init__('Validate Signature')

        layout = self.layout()

        select_document_button = QPushButton('Select Document')
        select_document_button.clicked.connect(self._select_document)
        layout.addWidget(select_document_button)

        select_xml_signature_button = QPushButton('Select XML Signature')
        select_xml_signature_button.clicked.connect(self._select_xml_signature)
        layout.addWidget(select_xml_signature_button)

        select_public_key_button = QPushButton('Select Public Key')
        select_public_key_button.clicked.connect(self._select_public_key)
        layout.addWidget(select_public_key_button)

        sign_button = QPushButton('Validate')
        sign_button.clicked.connect(self._validate_and_accept)
        layout.addWidget(sign_button)

        self._document_path = None
        self._xml_signature_path = None
        self._public_key_path = None

    def extract_values(self):
        return {
            'document_path': self._document_path,
            'xml_signature_path': self._xml_signature_path,
            'public_key_path': self._public_key_path,
        }

    def _select_document(self):
        self._document_path = self._select_file('All Files (*)')
        if not self._document_path:
            self._show_error('Please select a document file.')

    def _select_xml_signature(self):
        self._xml_signature_path = self._select_file('Select Signature Files (*.xml)')
        if not self._xml_signature_path:
            self._show_error('Please select an XML signature file.')

    def _select_public_key(self):
        self._public_key_path = self._select_file('Public Key Files (*.pem)')
        if not self._public_key_path:
            self._show_error('Please select a public key file.')

    def _validate_and_accept(self):
        conditions = [
            (lambda: self._document_path, 'Please select a document file.'),
            (lambda: self._xml_signature_path, 'Please select an XML signature file.'),
            (lambda: self._public_key_path, 'Please select a public key file.'),
            (lambda: os.path.exists(self._document_path), 'Document file not found.'),
            (lambda: os.path.exists(self._xml_signature_path), 'XML signature file not found.'),
            (lambda: os.path.exists(self._public_key_path), 'Public key file not found.')
        ]
        if self._validate(conditions):
            self.accept()
