from uuid import UUID

from src.auth import utils as auth_utils
from src.auth.constants import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from src.config import settings
from src.users.schemas import UserPayload


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_seconds: int,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return auth_utils.encode_jwt(
        payload=jwt_payload,
        expire_seconds=expire_seconds,
    )


def create_access_token(user_id: UUID) -> str:
    jwt_payload = {"sub": str(user_id)}
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_seconds=settings.auth_jwt.access_token_expire_seconds,
    )


def create_refresh_token(user_id: UUID) -> str:
    jwt_payload = {
        "sub": str(user_id),
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_seconds=settings.auth_jwt.refresh_token_expire_minutes,
    )


def get_user_payload_schema(
    payload: dict,
) -> UserPayload:
    payload["id"] = payload.pop("sub")
    return UserPayload(**payload)
