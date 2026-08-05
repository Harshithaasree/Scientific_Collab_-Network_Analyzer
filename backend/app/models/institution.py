from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from app.core import Base
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .researcher import Researcher


class Institution(Base):
    __tablename__: str = "institutions"

    institution_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    country: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    website: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    researchers: Mapped[list[Researcher]] = relationship(
        "Researcher",
        back_populates="institution",
    )

    def __repr__(self) -> str:
        return f"<Institution(id={self.institution_id}, name={self.name})>"