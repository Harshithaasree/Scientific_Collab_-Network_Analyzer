import logging

from core.security import hash_password
from fastapi import HTTPException
from models import User
from schemas import UserRequest, UserResponse, UserUpdateRequest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

logger: logging.Logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def register(self, credentials: UserRequest) -> User:
        logger.info("registering user: %s", credentials.email)
        existing: User | None = await self.get_user_by_email(credentials.email)
        if existing:
            logger.warning("registration failed, user exists: %s", credentials.email)
            raise HTTPException(status_code=409, detail="user already exists")

        new_user = User(email=credentials.email, password=credentials.password)
        self.session.add(new_user)
        await self.session.commit()
        logger.info("user registered successfully: %s", credentials.email)
        return new_user

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.session.scalar(select(User).where(User.email == email))

    async def update(self, credentials: UserUpdateRequest, user: User) -> UserResponse:
        logger.info("updating user: %s", user.email)
        updates = credentials.model_dump(exclude_none=True)
        if UserUpdateRequest.PASSWROD_FIELD in updates:
            user.password = hash_password(updates.pop(UserUpdateRequest.PASSWROD_FIELD))

        for key, val in updates.items():
            setattr(user, key, val)
        await self.session.commit()
        logger.info("user updated successfully: %s", user.email)
        return UserResponse.from_orm(user)

    async def delete(self, user: User) -> None:
        logger.info("deleting user: %s", user.email)
        await self.session.delete(user)
        await self.session.commit()
        logger.warning("user deleted: %s", user.email)
