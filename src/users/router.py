from uuid import UUID

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import dependencies as auth_dependencies
from src.database import database
from src.subscribes.schemas import SubscribeOut
from src.users import service as users_service
from src.users import utils as users_utils
from src.users.schemas import UserPayload, UserOut

router = APIRouter()


@router.get(
    path="/me",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
)
async def me(
    payload: dict = Depends(auth_dependencies.validate_access_token),
    session: AsyncSession = Depends(database.session_dependency),
):
    user_payload: UserPayload = users_utils.get_user_payload_schema(payload=payload)
    return await users_service.get_user(
        user_id=user_payload.id,
        session=session,
    )


@router.get(
    path="",
    response_model=list[UserOut],
    status_code=status.HTTP_200_OK,
)
async def get_users(
    payload: dict = Depends(auth_dependencies.validate_access_token),
    session: AsyncSession = Depends(database.session_dependency),
):
    return await users_service.get_users(
        session=session,
    )


@router.get(
    path="/me/followers",
    response_model=list[SubscribeOut],
    status_code=status.HTTP_200_OK,
)
async def get_followers(
    payload: dict = Depends(auth_dependencies.validate_access_token),
    session: AsyncSession = Depends(database.session_dependency),
):
    user_payload: UserPayload = users_utils.get_user_payload_schema(
        payload=payload,
    )
    return await users_service.get_followers(
        user_id=user_payload.id,
        session=session,
    )


@router.get(
    path="/me/following",
    response_model=list[SubscribeOut],
    status_code=status.HTTP_200_OK,
)
async def get_followers(
    payload: dict = Depends(auth_dependencies.validate_access_token),
    session: AsyncSession = Depends(database.session_dependency),
):
    user_payload: UserPayload = users_utils.get_user_payload_schema(
        payload=payload,
    )
    return await users_service.get_following(
        user_id=user_payload.id,
        session=session,
    )


@router.get(
    path="/{user_id}/followers",
    response_model=list[SubscribeOut],
    status_code=status.HTTP_200_OK,
)
async def get_user_followers(
    user_id: UUID,
    payload: dict = Depends(auth_dependencies.validate_access_token),
    session: AsyncSession = Depends(database.session_dependency),
):
    return await users_service.get_followers(
        user_id=user_id,
        session=session,
    )


@router.get(
    path="/{user_id}/following",
    response_model=list[SubscribeOut],
    status_code=status.HTTP_200_OK,
)
async def get_user_following(
    user_id: UUID,
    payload: dict = Depends(auth_dependencies.validate_access_token),
    session: AsyncSession = Depends(database.session_dependency),
):
    return await users_service.get_following(
        user_id=user_id,
        session=session,
    )
