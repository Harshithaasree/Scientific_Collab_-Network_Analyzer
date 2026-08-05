from fastapi import APIRouter
from app.schemas import UserResponse, UserUpdateRequest

from .deps import CurrentUser, UserServiceDeps

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.patch("/me")
async def update_me(
    credential: UserUpdateRequest,
    current_user: CurrentUser,
    user_service: UserServiceDeps,
) -> UserResponse:
    return await user_service.update(credential, current_user)


@user_router.delete("/me", status_code=204)
async def delete_me(
    current_user: CurrentUser,
    user_service: UserServiceDeps,
) -> None:
    await user_service.delete(current_user)
