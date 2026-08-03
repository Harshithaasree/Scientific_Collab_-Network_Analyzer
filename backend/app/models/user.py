from core import Base
from core.constants import PASSWORD_MAX_LENGTH, USERNAME_MAX_LENGTH
from core.security import hash_password, verify_password
from pydantic import SecretStr
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__: str = "users"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(PASSWORD_MAX_LENGTH), nullable=False)
    user_name: Mapped[str | None] = mapped_column(
        String(USERNAME_MAX_LENGTH), nullable=True, default=None
    )

    def __init__(
        self, email: str, password: SecretStr, user_name: str | None = None
    ) -> None:
        self.email = email
        self.password = hash_password(password)
        self.user_name = user_name

    def check_password(self, plain_password) -> bool:
        return verify_password(plain_password, self.password)

    def __repr__(self) -> str:
        return f"<User(email={self.email}, name={self.user_name})>"
