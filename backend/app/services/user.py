from core.security import hash_password
from fastapi import HTTPException
from models import User
from schemas import UserRequest, UserResponse, UserUpdateRequest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def register(self, credentials: UserRequest) -> User:
        existing: User | None = await self.get_user_by_email(credentials.email)
        if existing:
            raise HTTPException(status_code=409, detail="user already exists")

        new_user = User(
            email=credentials.email,
            password=credentials.password,
            user_name=credentials.user_name,
        )
        self.session.add(new_user)
        await self.session.commit()
        return new_user

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.session.scalar(select(User).where(User.email == email))

    async def update(self, credentials: UserUpdateRequest, user: User) -> UserResponse:
        updates = credentials.model_dump(exclude_none=True)
        if UserUpdateRequest.PASSWROD_FIELD in updates:
            user.password = hash_password(updates.pop(UserUpdateRequest.PASSWROD_FIELD))
        for key, val in updates.items():
            setattr(user, key, val)
        await self.session.commit()
        return UserResponse.from_orm(user)

    async def delete(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.commit()
