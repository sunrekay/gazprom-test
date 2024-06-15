from datetime import date
from typing import Annotated
from uuid import UUID

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr

from src.users.constants import PASSWORD_LENGTH_MIN, PASSWORD_LENGTH_MAX


class UserSchema(BaseModel):
    id: UUID
    email: EmailStr
    password: Annotated[
        str,
        MinLen(PASSWORD_LENGTH_MIN),
        MaxLen(PASSWORD_LENGTH_MAX),
    ]
    birthday: date


class UserPayload(BaseModel):
    id: UUID


class UserRegistrationIn(BaseModel):
    email: EmailStr
    password: Annotated[
        str,
        MinLen(PASSWORD_LENGTH_MIN),
        MaxLen(PASSWORD_LENGTH_MAX),
    ]
    birthday: date


class UserRegistrationOut(BaseModel):
    id: UUID
    email: EmailStr


class UserLoginIn(BaseModel):
    email: EmailStr
    password: Annotated[
        str,
        MinLen(PASSWORD_LENGTH_MIN),
        MaxLen(PASSWORD_LENGTH_MAX),
    ]


class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    birthday: date
