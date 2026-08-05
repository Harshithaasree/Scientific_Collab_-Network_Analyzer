from fastapi import APIRouter
from schemas import UserResponse, UserUpdateRequest

from .deps import AdminUser, CurrentUser, UserServiceDeps

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


@user_router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int, adim: AdminUser, user_service: UserServiceDeps
) -> None:
    await user_service.delete_by_id(user_id)
