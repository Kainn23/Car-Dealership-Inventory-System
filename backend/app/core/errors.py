"""Domain exception classes."""


class AppError(Exception):
    """Base application domain error."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class InvalidTokenError(AppError):
    """Raised when a JWT is expired, tampered, or malformed."""

    def __init__(self, message: str = "Invalid or expired token") -> None:
        super().__init__(message=message, code="INVALID_TOKEN")


class UserAlreadyExistsError(AppError):
    """Raised when registering an email that already exists."""

    def __init__(self, message: str = "User with this email already exists") -> None:
        super().__init__(message=message, code="EMAIL_ALREADY_EXISTS")


class InvalidCredentialsError(AppError):
    """Raised on invalid login credentials."""

    def __init__(self, message: str = "Invalid email or password") -> None:
        super().__init__(message=message, code="INVALID_CREDENTIALS")


class InsufficientPermissionsError(AppError):
    """Raised when a user lacks required role permissions."""

    def __init__(self, message: str = "Insufficient permissions") -> None:
        super().__init__(message=message, code="FORBIDDEN")
