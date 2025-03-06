from uuid import uuid4

from sqlalchemy import UUID, Unicode
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.database.mixins import TimeStampMixin, UserAuditMixin


class Category(Base, UserAuditMixin, TimeStampMixin):
    __tablename__ = "categories"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid4
    )
    name: Mapped[str] = mapped_column(Unicode(128), nullable=False, unique=True)

    def __str__(self):
        return f"uuid: {self.uuid}, name: {self.name}"

    def __repr__(self):
        return self.__str__()
