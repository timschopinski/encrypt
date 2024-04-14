from common.backend.exceptions import EncryptException


class DocumentSigningError(EncryptException):
    message = 'Failed to sign the document.'


class SigningValidationError(EncryptException):
    message = 'Failed to validate the signing'


class InvalidPinError(EncryptException):
    message = 'Invalid pin provided.'
