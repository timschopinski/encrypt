from enum import Enum, StrEnum


class RSABits(Enum):
    BITS_1024 = 1024
    BITS_2048 = 2048
    BITS_4096 = 4096


class DSABits(Enum):
    BITS_1024 = 1024
    BITS_2048 = 2048
    BITS_3072 = 3072


class Algorithm(StrEnum):
    RSA = 'RSA'
    DSA = 'DSA'
