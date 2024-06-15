from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class Subscribe(Base):
    __tablename__ = "subscribe"
    __table_args__ = (
        UniqueConstraint(
            "follower_id",
            "following_id",
            name="idx_unique_subscribe",
        ),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    follower_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    following_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))

    follower = relationship("User", foreign_keys=[follower_id])
    following = relationship("User", foreign_keys=[following_id])
