from uuid import uuid4

from sqlalchemy import UUID, Enum, Text, Unicode
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.database.mixins import TimeStampMixin, UserAuditMixin
from app.schemas.post import PostStatus


class Post(Base, UserAuditMixin, TimeStampMixin):
    __tablename__ = "posts"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid4
    )
    title: Mapped[str] = mapped_column(Unicode(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[PostStatus] = mapped_column(
        Enum(PostStatus, create_type=False), nullable=False, default=PostStatus.DRAFT
    )

    def __str__(self):
        return f"uuid: {self.uuid}, title: {self.title}"

    def __repr__(self):
        return self.__str__()
