from uuid import uuid4

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.database.mixins import TimeStampMixin, UserAuditMixin


class PostCategory(Base, TimeStampMixin, UserAuditMixin):
    __tablename__ = "post_categories"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, primary_key=True, unique=True, default=uuid4
    )
    post_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("posts.uuid"), nullable=False
    )
    category_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.uuid"), nullable=True
    )
    sub_category_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sub_categories.uuid"), nullable=True
    )

    def __str__(self):
        return f"uuid: {self.uuid}, post_id: {self.post_id}"

    def __repr__(self):
        return self.__str__()
