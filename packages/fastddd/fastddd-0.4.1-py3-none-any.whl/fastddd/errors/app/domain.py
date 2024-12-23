from pydantic import ValidationError
from .base import AppBaseException
from ...libs.pydantic_validation_handler import convert_pydantic_exception


class DomainException(AppBaseException):
    def __init__(self, message: str, error_code: str):
        super().__init__(message, error_code)


class DomainServiceException(DomainException):
    def __init__(self, message: str, error_code: str):
        super().__init__(message, error_code)


class ValidationException(DomainException):
    def __init__(self, e: ValidationError, message: str, error_code: str, object_name: str | None = None):
        self.multi_validate_errors = convert_pydantic_exception(e, object_name)
        super().__init__(message, error_code)


class RootModelValidationException(ValidationException):
    def __init__(self, e: ValidationError, message: str, error_code: str, object_name: str):
        super().__init__(e, message, error_code, object_name)
