from uuid import UUID

from pydantic import BaseModel


class SubscribeOut(BaseModel):
    follower_id: UUID
    following_id: UUID
