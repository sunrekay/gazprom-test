from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.subscribes.models import Subscribe
from src.users import exceptions as users_exceptions
from src.users.models import User
from src.users.schemas import UserRegistrationIn


async def create_user(
    user_in: UserRegistrationIn,
    session: AsyncSession,
) -> User:
    try:
        user: User = User(**user_in.model_dump())
        session.add(user)
        await session.commit()
        return user
    except IntegrityError:
        await session.rollback()
        raise users_exceptions.user_already_exist


async def get_user(
    user_id: UUID,
    session: AsyncSession,
) -> Optional[User]:
    return await session.get(User, user_id)


async def get_users(
    session: AsyncSession,
) -> list[User]:
    result = await session.scalars(select(User))
    return list(result.all())


async def get_user_by_email(
    user_email: str,
    session: AsyncSession,
) -> Optional[User]:
    user = await session.scalar(
        select(User).where(
            User.email == user_email,
        )
    )
    return user


async def get_followers(
    user_id: UUID,
    session: AsyncSession,
) -> list[Subscribe]:
    followers = await session.scalars(
        select(Subscribe).where(
            Subscribe.following_id == user_id,
        )
    )
    return list(followers.all())


async def get_following(
    user_id: UUID,
    session: AsyncSession,
):
    following = await session.scalars(
        select(Subscribe).where(
            Subscribe.follower_id == user_id,
        )
    )
    return list(following.all())
