import asyncio

from app.core import Base, engine
from app.models import (
    Citation,
    Collaboration,
    Conference,
    Institution,
    Project,
    ProjectResearcher,
    Publication,
    PublicationAuthor,
    Researcher,
    RevokedToken,
    User,
)


async def create_tables() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    print("Database tables created successfully!")


if __name__ == "__main__":
    asyncio.run(create_tables())