import os
import datetime
from Crypto.Cipher import AES
from hashlib import sha256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from lxml import etree


class DocumentSigner:
    def __init__(self, encrypted_private_key_path: str):
        self.encrypted_private_key_path = encrypted_private_key_path

    def sign_document(self, file_path: str, pin: str, username: str) -> tuple[bytes | None, bool]:
        try:
            with open(self.encrypted_private_key_path, 'rb') as key_file:
                key_data = key_file.read()
                nonce = key_data[:16]
                tag = key_data[16:32]
                ciphertext = key_data[32:]
                cipher_aes = AES.new(sha256(pin.encode()).digest(), AES.MODE_EAX, nonce=nonce)
                private_key_data = cipher_aes.decrypt_and_verify(ciphertext, tag)

            private_key = RSA.import_key(private_key_data)

            with open(file_path, 'rb') as file:
                document_content = file.read()

            document_hash = SHA256.new(document_content).hexdigest()
            cipher_rsa = PKCS1_OAEP.new(private_key)
            encrypted_hash = cipher_rsa.encrypt(document_hash.encode())

            xml_signature = self._generate_xml_signature(file_path, encrypted_hash, username)

            if isinstance(xml_signature, str):
                xml_signature = xml_signature.encode()

            signature_file_path = self._generate_signature_file_path(file_path)
            with open(signature_file_path, 'wb') as signature_file:
                signature_file.write(xml_signature)

            return xml_signature, True

        except Exception:
            return None, False

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

        return etree.tostring(xml_signature, encoding='unicode', pretty_print=True)

    @staticmethod
    def _generate_signature_file_path(file_path: str) -> str:
        signature_file_path = os.path.splitext(file_path)[0] + '_signature.xml'
        return signature_file_path
