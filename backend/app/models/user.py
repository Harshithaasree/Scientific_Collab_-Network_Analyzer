from __future__ import annotations

from typing import TYPE_CHECKING

from app.core import Base
from app.core.constants import PASSWORD_MAX_LENGTH
from app.core.security import hash_password, verify_password
from pydantic import SecretStr
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .researcher import Researcher


class User(Base):
    __tablename__: str = "users"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(PASSWORD_MAX_LENGTH), nullable=False)

    researcher: Mapped[Researcher | None] = relationship(
    "Researcher",
    back_populates="user",
    uselist=False,
)

    def __init__(self, email: str, password: SecretStr) -> None:
        self.email = email
        self.password = hash_password(password)

    def check_password(self, plain_password) -> bool:
        return verify_password(plain_password, self.password)

    def __repr__(self) -> str:
        return f"<User(email={self.email})>"
