from typing import Final

PASSWORD_MIN_LENGTH: Final[int] = 8
PASSWORD_MAX_LENGTH: Final[int] = 128
USERNAME_MAX_LENGTH: Final[int] = 100

ALLOWED_EMAIL_DOMAINS: Final[frozenset[str]] = frozenset(
    {
        "gmail.com",
        "outlook.com",
        "yahoo.com",
        "hotmail.com",
        "icloud.com",
        "protonmail.com",
    }
)


class TokenFields:
    SUBJECT: Final[str] = "sub"
    TYPE: Final[str] = "type"
    EXPIRY: Final[str] = "exp"


class TokenType:
    ACCESS: Final[str] = "access"
    REFRESH: Final[str] = "refresh"
    BEARER: Final[str] = "bearer"
