from typing import Final

PASSWORD_MIN_LENGTH: Final[int] = 8
PASSWORD_MAX_LENGTH: Final[int] = 128
USERNAME_MAX_LENGTH: Final[int] = 100


class TokenFields:
    SUBJECT: Final[str] = "sub"
    TYPE: Final[str] = "type"
    EXPIRY: Final[str] = "exp"


class TokenType:
    ACCESS: Final[str] = "access"
    REFRESH: Final[str] = "refresh"
    BEARER: Final[str] = "bearer"
