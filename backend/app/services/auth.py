from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import RevokedToken, User
from app.schemas import TokenResponse, UserRequest
from app.services.token import TokenService
from app.services.user import UserService


class AuthService:
    def __init__(self, token_service: TokenService) -> None:
        self.token_service = token_service

    def login_registered_user(
        self,
        user: User,
    ) -> TokenResponse:

        access_token = self.token_service.create_access_token(
            user.email
        )

        refresh_token = self.token_service.create_refresh_token(
            user.email
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    async def login(
        self,
        credentials: UserRequest,
        user_service: UserService,
    ) -> TokenResponse:

        user = await user_service.get_user_by_email(
            str(credentials.email)
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="invalid email or password",
            )

        if not user.check_password(
            credentials.password
        ):
            raise HTTPException(
                status_code=401,
                detail="invalid email or password",
            )

        return self.login_registered_user(user)

    async def logout(
        self,
        refresh_token: str,
        session: AsyncSession,
    ) -> None:

        payload = self.token_service.decode_token(
            refresh_token
        )

        if payload.token_type != "refresh":
            raise HTTPException(
                status_code=400,
                detail="invalid refresh token",
            )

        existing = await session.scalar(
            select(RevokedToken).where(
                RevokedToken.token == refresh_token
            )
        )

        if not existing:
            session.add(
                RevokedToken(
                    token=refresh_token
                )
            )

            await session.commit()

    async def refresh(
        self,
        refresh_token: str,
        user_service: UserService,
        session: AsyncSession,
    ) -> TokenResponse:

        payload = self.token_service.decode_token(
            refresh_token
        )

        if payload.token_type != "refresh":
            raise HTTPException(
                status_code=400,
                detail="invalid refresh token",
            )

        revoked = await session.scalar(
            select(RevokedToken).where(
                RevokedToken.token == refresh_token
            )
        )

        if revoked:
            raise HTTPException(
                status_code=401,
                detail="refresh token has been revoked",
            )

        user = await user_service.get_user_by_email(
            payload.sub
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="user not found",
            )

        return self.login_registered_user(user)

