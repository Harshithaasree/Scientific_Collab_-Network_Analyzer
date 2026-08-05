from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING


from .collaboration import Collaboration
from .project import Project
from .publication import Publication

from app.core import Base
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .user import User

if TYPE_CHECKING:
    from .institution import Institution
    from .user import User


class Researcher(Base):
    __tablename__: str = "researchers"

    researcher_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    institution_id: Mapped[int | None] = mapped_column(
        ForeignKey("institutions.institution_id"),
        nullable=True,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    affiliation: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    research_area: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    bio: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    user: Mapped[User] = relationship(
        "User",
        back_populates="researcher",
        uselist=False,
    )

    institution: Mapped[Institution | None] = relationship(
        "Institution",
        back_populates="researchers",
    )
    publications: Mapped[list[Publication]] = relationship(
    "Publication",
    secondary="publication_authors",
    back_populates="authors",
)

    projects: Mapped[list[Project]] = relationship(
    "Project",
    secondary="project_researchers",
    back_populates="researchers",
)

    collaborations_as_researcher_1: Mapped[list[Collaboration]] = relationship(
    "Collaboration",
    foreign_keys="Collaboration.researcher_id_1",
    back_populates="researcher_1",
)

    collaborations_as_researcher_2: Mapped[list[Collaboration]] = relationship(
    "Collaboration",
    foreign_keys="Collaboration.researcher_id_2",
    back_populates="researcher_2",
)

    def __repr__(self) -> str:
        return (
            f"<Researcher("
            f"id={self.researcher_id}, "
            f"name={self.first_name} {self.last_name}"
            f")>"
        )