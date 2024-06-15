from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from src.auth import exceptions as auth_exceptions
from src.auth import utils as auth_utils
from src.auth.constants import OAuth2PasswordBearer_tokenUrl
from src.auth.constants import TOKEN_TYPE_FIELD, REFRESH_TOKEN_TYPE, ACCESS_TOKEN_TYPE

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=OAuth2PasswordBearer_tokenUrl,
)


def token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
        return payload

    except InvalidTokenError:
        raise auth_exceptions.token_invalid


def validate_access_token(
    payload: dict = Depends(token_payload),
) -> dict:
    token_type: str = payload.get(TOKEN_TYPE_FIELD)
    if token_type == ACCESS_TOKEN_TYPE:
        return payload

    else:
        raise auth_exceptions.token_invalid


def validate_refresh_token(
    payload: dict = Depends(token_payload),
) -> dict:
    token_type: str = payload.get(TOKEN_TYPE_FIELD)
    if token_type == REFRESH_TOKEN_TYPE:
        return payload

    else:
        raise auth_exceptions.token_invalid
