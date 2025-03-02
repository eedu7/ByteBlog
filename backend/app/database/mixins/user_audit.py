from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, declared_attr, mapped_column


class UserAuditMixin:
    """Mixin class to add created_by, updated_by and deleted_by to models."""

    @declared_attr
    def created_by(cls) -> Mapped[UUID]:
        return mapped_column(
            UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=True
        )

    @declared_attr
    def updated_by(cls) -> Mapped[UUID]:
        return mapped_column(
            UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=True
        )

    @declared_attr
    def deleted_by(cls) -> Mapped[UUID | None]:
        return mapped_column(
            UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=True
        )
