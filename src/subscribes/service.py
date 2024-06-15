from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import and_

from src.subscribes import exceptions as subscribes_exceptions
from src.subscribes.models import Subscribe
from src.users.schemas import UserPayload


async def create_subscribe(
    user_payload: UserPayload,
    following_id: UUID,
    session: AsyncSession,
):
    try:
        subscribe: Subscribe = Subscribe(
            follower_id=user_payload.id,
            following_id=following_id,
        )
        session.add(subscribe)
        await session.commit()
        return subscribe
    except IntegrityError:
        await session.rollback()
        raise subscribes_exceptions.subscribe_already_exist


async def delete_subscribe(
    user_payload: UserPayload,
    following_id: UUID,
    session: AsyncSession,
):
    await session.execute(
        delete(Subscribe).where(
            and_(
                Subscribe.following_id == following_id,
                Subscribe.follower_id == user_payload.id,
            )
        )
    )
    await session.commit()
