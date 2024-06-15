from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import utils as auth_utils
from src.auth.schemas import TokensInfo
from src.users import service as user_service
from src.users import utils as user_utils
from src.users.models import User
from src.users.schemas import UserRegistrationIn, UserPayload


async def registration(
    user_in: UserRegistrationIn,
    session: AsyncSession,
) -> User:
    user_in.password = auth_utils.hash_password(password=user_in.password)
    user = await user_service.create_user(
        user_in=user_in,
        session=session,
    )
    return user


def login(user: User) -> TokensInfo:
    access_token = user_utils.create_access_token(user_id=user.id)
    refresh_token = user_utils.create_refresh_token(user_id=user.id)
    return TokensInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


def refresh(payload: dict) -> TokensInfo:
    user_payload: UserPayload = user_utils.get_user_payload_schema(payload=payload)
    access_token = user_utils.create_access_token(user_id=user_payload.id)
    return TokensInfo(access_token=access_token)
