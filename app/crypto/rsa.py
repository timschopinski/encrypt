from Crypto.PublicKey import RSA
import os


class RSAKeys:

    def __init__(self, default_directory: str = None):
        self.default_directory = default_directory

    def create(self, key_name: str, bits: int = 4096, directory: str = None) -> None:
        key = RSA.generate(bits)
        private_key_path, public_key_path = self._generate_paths(key_name, directory)

        with open(private_key_path, 'wb') as private_key_file:
            private_key_file.write(key.export_key())

        with open(public_key_path, 'wb') as public_key_file:
            public_key_file.write(key.publickey().export_key())

    def _generate_paths(self, key_name: str, directory: str = None) -> tuple:
        save_directory = directory or self.default_directory or "."
        private_key_path = os.path.join(save_directory, f'{key_name}_private_key.pem')
        public_key_path = os.path.join(save_directory, f'{key_name}_public_key.pem')
        return private_key_path, public_key_path
