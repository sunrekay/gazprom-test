from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import dependencies as auth_dependencies
from src.auth import service as auth_service
from src.auth.schemas import TokensInfo
from src.database import database
from src.users import dependencies as user_dependencies
from src.users.models import User
from src.users.schemas import (
    UserRegistrationIn,
    UserRegistrationOut,
)

router = APIRouter()


@router.post(
    path="/registration",
    response_model=UserRegistrationOut,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
async def registration(
    user_in: UserRegistrationIn,
    session: AsyncSession = Depends(database.session_dependency),
):
    return await auth_service.registration(
        user_in=user_in,
        session=session,
    )


@router.post(
    path="/login",
    response_model=TokensInfo,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
def login(
    user: User = Depends(user_dependencies.verify_login),
):
    return auth_service.login(user=user)


@router.get(
    path="/refresh",
    response_model=TokensInfo,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
def refresh(
    payload: dict = Depends(auth_dependencies.validate_refresh_token),
):
    return auth_service.refresh(
        payload=payload,
    )
