from common.backend.exceptions import EncryptException


class PasswordLookupError(EncryptException):
    message = 'Failed to lookup the file.'

