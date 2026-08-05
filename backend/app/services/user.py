import logging

from app.core.security import hash_password
from app.models import User
from app.schemas import UserRequest, UserResponse, UserUpdateRequest
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

logger: logging.Logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def register(self, credentials: UserRequest) -> User:
        logger.info("registering user: %s", credentials.email)

        existing: User | None = await self.get_user_by_email(
            str(credentials.email)
        )

        if existing:
            logger.warning(
                "registration failed, user exists: %s",
                credentials.email,
            )
            raise HTTPException(
                status_code=409,
                detail="user already exists",
            )

        new_user = User(
            email=str(credentials.email),
            password=credentials.password,
        )

        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        logger.info(
            "user registered successfully: %s",
            credentials.email,
        )

        return new_user

    async def get_user_by_email(
        self,
        email: str,
    ) -> User | None:
        result = await self.session.scalar(
            select(User).where(User.email == email)
        )

        return result

    async def get_user_by_id(
        self,
        user_id: int,
    ) -> User | None:
        result = await self.session.scalar(
            select(User).where(User.user_id == user_id)
        )

        return result

    async def update(
        self,
        credentials: UserUpdateRequest,
        user: User,
    ) -> UserResponse:
        logger.info("updating user: %s", user.email)

        updates = credentials.model_dump(
            exclude_none=True,
        )

        if UserUpdateRequest.PASSWORD_FIELD in updates:
            password = updates.pop(
                UserUpdateRequest.PASSWORD_FIELD
            )

            user.password = hash_password(password)

        for key, value in updates.items():
            setattr(user, key, value)

        await self.session.commit()
        await self.session.refresh(user)

        logger.info(
            "user updated successfully: %s",
            user.email,
        )

        return UserResponse.from_orm(user)

    async def delete(self, user: User) -> None:
        logger.info(
            "deleting user: %s",
            user.email,
        )

        await self.session.delete(user)
        await self.session.commit()

        logger.warning(
            "user deleted: %s",
            user.email,
        )

