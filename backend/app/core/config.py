import os

from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

class Config:
    JWT_KEY = SecretStr(os.environ.get("JWT_KEY", ""))
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "")
    ALGORITHM: str = os.environ.get("ALGORITHM", "HS256")
    ACCESS_TOKEN_TIME_MINUTES = int(os.environ.get("ACCESS_TOKEN_TIME_MINUTES", "0"))

    @classmethod
    def validate(cls) -> None:
        """Validate that all required configuration variables are set"""
        errors: list[str] = []
        if not cls.JWT_KEY.get_secret_value():
            errors.append("JWT_KEY is not set")
        if not cls.DATABASE_URL:
            errors.append("DATABASE_URL is not set")
        if not cls.ALGORITHM in ("HS256", "HS384", "HS512"):
            errors.append(
                f"ALGORITHM '{cls.ALGORITHM}' is not a supported HMAC algorithm"
            )
        if not cls.ACCESS_TOKEN_TIME_MINUTES <= 0:
            errors.append("ACCESS_TOKEN_TIME_MINUTES must be a positive integer")

        if errors:
            raise SystemExit(
                f"configuration error:-\n{'\n'.join(f'- {error}' for error in errors)}"
            )


class DevelopmentConfig(Config):
    SECRET_KEY: SecretStr = SecretStr("dev-key")
    DATABASE_URL: str = os.environ.get("DEV_DATABASE_URL", "sqlite:///./dev_bet.db")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


class TestingConfig(Config):
    SECRET_KEY = SecretStr("test-key")
    DATABASE_URL: str = os.environ.get("TEST_DATABASE_URL", "sqlite:///./test_bet.db")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


class ProductionConfig(Config):
    pass


config: dict[str, type[Config]] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config() -> type[Config]:
    env: str = os.environ.get("FASTAPI_ENV", "development")
    if env not in config:
        raise SystemExit(
            f"[config] FASTAPI_ENV must be in {list(config.keys())}, got '{env}'"
        )
    return config[env]
