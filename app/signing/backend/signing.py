import datetime
from typing import Any

from Crypto.Cipher import AES
from hashlib import sha256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from lxml import etree
import os


class DocumentSigner:
    def __init__(self, encrypted_private_key_path: str):
        self.encrypted_private_key_path = encrypted_private_key_path

    def sign_document(self, file_path: str, pin: str, username: str) -> tuple[bytes | None, bool]:
        try:
            private_key = self._get_private_key(pin)
            document_content = self._get_document_content(file_path)
            document_hash = SHA256.new(document_content)
            cipher_rsa = PKCS1_v1_5.new(private_key)
            encrypted_hash = cipher_rsa.sign(document_hash)

            xml_signature = self._generate_xml_signature(file_path, encrypted_hash, username)
            self._save_signature(xml_signature, file_path)
            return xml_signature, True

        except Exception:
            return None, False

    @staticmethod
    def _get_document_content(file_path: str) -> bytes:
        with open(file_path, 'rb') as file:
            document_content = file.read()
        return document_content

    def _save_signature(self, xml_signature: bytes, file_path: str) -> None:
        signature_file_path = self._generate_signature_file_path(file_path)
        with open(signature_file_path, 'wb') as signature_file:
            signature_file.write(xml_signature)

    def _get_private_key(self, pin: str):
        with open(self.encrypted_private_key_path, 'rb') as key_file:
            key_data = key_file.read()
            nonce = key_data[:16]
            tag = key_data[16:32]
            ciphertext = key_data[32:]
            cipher_aes = AES.new(sha256(pin.encode()).digest(), AES.MODE_EAX, nonce=nonce)
            private_key_data = cipher_aes.decrypt_and_verify(ciphertext, tag)

        return RSA.import_key(private_key_data)

    @staticmethod
    def _generate_xml_signature(file_path: str, encrypted_hash: bytes, username: str) -> bytes:
        xml_signature = etree.Element('Signature')
        document_info = etree.SubElement(xml_signature, 'DocumentInfo')
        document_info.text = os.path.basename(file_path)

        document_info.set('size', str(os.path.getsize(file_path)))
        document_info.set('extension', os.path.splitext(file_path)[-1])
        document_info.set('modification_date',
                          datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S'))

        user_info = etree.SubElement(xml_signature, 'UserInfo')
        user_info.text = username
        encrypted_hash_element = etree.SubElement(xml_signature, 'EncryptedHash')
        encrypted_hash_element.text = encrypted_hash.hex()
        timestamp = etree.SubElement(xml_signature, 'Timestamp')
        timestamp.text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        xml_signature = etree.tostring(xml_signature, encoding='unicode', pretty_print=True)

        if isinstance(xml_signature, str):
            xml_signature = xml_signature.encode()

        return xml_signature

    @staticmethod
    def _generate_signature_file_path(file_path: str) -> str:
        signature_file_path = os.path.splitext(file_path)[0] + '_signature.xml'
        return signature_file_path


class SignatureValidator:
    def validate_signature(self, document_path: str, xml_signature_path: str, public_key_path: str) -> tuple[bool, Any]:
        try:
            with open(document_path, 'rb') as file:
                document_content = file.read()

            document_hash = SHA256.new(document_content)

            with open(xml_signature_path, 'r') as xml_file:
                xml_content = xml_file.read()

            xml_signature = etree.fromstring(xml_content)
            encrypted_hash_hex = xml_signature.findtext('EncryptedHash')
            document_info = self._get_document_info(xml_signature)
            with open(public_key_path, 'rb') as key_file:
                key_data = key_file.read()
                public_key = RSA.import_key(key_data)

            encrypted_hash = bytes.fromhex(encrypted_hash_hex)

            result = PKCS1_v1_5.new(public_key).verify(document_hash, encrypted_hash)
            return result, document_info

        except Exception:
            return False, None

    @staticmethod
    def _get_document_info(xml_signature) -> str:
        signature_info = xml_signature.find('DocumentInfo')
        size = int(signature_info.get('size', 'Not Found'))
        modification_date = signature_info.get('modification_date', 'Not Found')
        document_name = signature_info.text
        username = xml_signature.findtext('UserInfo', 'Not Found')
        timestamp = xml_signature.findtext('Timestamp')
        document_info = f'''
            Document name: {document_name}\n
            Document size: {size}b\n
            Document modification: {modification_date}\n
            Username: {username}\n
            Timestamp: {timestamp}\n
        '''

        return document_info
