from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import utils as auth_utils
from src.database import database
from src.users import exceptions as user_exceptions
from src.users import service as user_service
from src.users.models import User
from src.users.schemas import UserLoginIn


async def verify_login(
    user_in: UserLoginIn,
    session: AsyncSession = Depends(database.session_dependency),
):
    user: User = await user_service.get_user_by_email(
        user_email=user_in.email,
        session=session,
    )

    if user is None:
        raise user_exceptions.wrong_email_or_password

    if not auth_utils.verify_password(
        password=user_in.password, hashed_password=user.password
    ):
        raise user_exceptions.wrong_email_or_password

    return user
