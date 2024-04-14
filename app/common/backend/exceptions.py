
class EncryptException(Exception):
    message = NotImplementedError()
    pass


class UnknownAlgorithmException(EncryptException):
    message = 'Unknown algorithm.'
