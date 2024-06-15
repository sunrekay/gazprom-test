from datetime import date
from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from src.models import Base
from src.users.constants import EMAIL_LENGTH


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    email: Mapped[str] = mapped_column(
        String(EMAIL_LENGTH), nullable=False, unique=True
    )
    password: Mapped[bytes] = mapped_column(nullable=False)
    birthday: Mapped[date] = mapped_column(nullable=False)
