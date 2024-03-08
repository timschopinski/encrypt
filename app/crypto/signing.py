import os
import datetime
import logging
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from lxml import etree


class DocumentSigner:
    def __init__(self, private_key_path):
        self.private_key_path = private_key_path
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def generate_xml_signature(self, file_path, encrypted_hash):
        xml_signature = etree.Element("Signature")
        document_info = etree.SubElement(xml_signature, "DocumentInfo")
        document_info.text = os.path.basename(file_path)
        user_info = etree.SubElement(xml_signature, "UserInfo")
        user_info.text = "User A"
        encrypted_hash_element = etree.SubElement(xml_signature, "EncryptedHash")
        encrypted_hash_element.text = encrypted_hash.decode()
        timestamp = etree.SubElement(xml_signature, "Timestamp")
        timestamp.text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return etree.tostring(xml_signature, pretty_print=True)

    def sign_document(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                document_content = file.read()

            document_hash = SHA256.new(document_content).hexdigest()

            with open(self.private_key_path, 'rb') as key_file:
                private_key = RSA.import_key(key_file.read())

            cipher_rsa = PKCS1_OAEP.new(private_key)
            encrypted_hash = cipher_rsa.encrypt(document_hash.encode())

            xml_signature = self.generate_xml_signature(file_path, encrypted_hash)
            self.logger.info(f"Document signed: {file_path}")
            return xml_signature
        except Exception as e:
            self.logger.error(f"Error signing document {file_path}: {e}")
            raise

    @staticmethod
    def parse_xml_signature(xml_signature):
        root = etree.fromstring(xml_signature)
        document_info = root.find("DocumentInfo").text
        user_info = root.find("UserInfo").text
        encrypted_hash = root.find("EncryptedHash").text
        timestamp = root.find("Timestamp").text

        return document_info, user_info, encrypted_hash, timestamp
