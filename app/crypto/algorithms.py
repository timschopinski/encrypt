from abc import ABC, abstractmethod
from typing import Optional

from Crypto.PublicKey import RSA, DSA


class Algorithm(ABC):
    @classmethod
    @abstractmethod
    def generate(cls, bits: int):
        pass

    @classmethod
    @abstractmethod
    def import_key(cls, extern_key: str | bytes, passphrase: Optional[str]=None):
        pass

    @classmethod
    def load_key(cls, key_path: str):
        with open(key_path, 'rb') as public_key_file:
            return cls.import_key(public_key_file.read())

    @classmethod
    def name(cls):
        return cls.__name__.replace('Algorithm', '').lower()


class RsaAlgorithm(Algorithm):

    @classmethod
    def generate(cls, bits: int):
        return RSA.generate(bits)

    @classmethod
    def import_key(cls, extern_key: str | bytes, passphrase: Optional[str]=None):
        return RSA.import_key(extern_key, passphrase)


class DsaAlgorithm(Algorithm):

    @classmethod
    def generate(cls, bits: int):
        return DSA.generate(bits)

    @classmethod
    def import_key(cls, extern_key: str | bytes, passphrase: Optional[str]=None):
        return DSA.import_key(extern_key, passphrase)
