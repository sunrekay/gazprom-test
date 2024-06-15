from uuid import UUID

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import dependencies as auth_dependencies
from src.database import database
from src.subscribes import service as subscribes_service
from src.subscribes.schemas import SubscribeOut
from src.users import utils as users_utils

router = APIRouter()


@router.post(
    path="",
    response_model=SubscribeOut,
    status_code=status.HTTP_201_CREATED,
)
async def subscribe(
    following_id: UUID,
    payload: dict = Depends(auth_dependencies.validate_access_token),
    session: AsyncSession = Depends(database.session_dependency),
):
    return await subscribes_service.create_subscribe(
        user_payload=users_utils.get_user_payload_schema(
            payload=payload,
        ),
        following_id=following_id,
        session=session,
    )


@router.delete(
    path="",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def unsubscribe(
    following_id: UUID,
    payload: dict = Depends(auth_dependencies.validate_access_token),
    session: AsyncSession = Depends(database.session_dependency),
):
    await subscribes_service.delete_subscribe(
        user_payload=users_utils.get_user_payload_schema(
            payload=payload,
        ),
        following_id=following_id,
        session=session,
    )
