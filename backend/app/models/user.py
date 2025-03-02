from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, DateTime, Text, Unicode, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.database.mixins import TimeStampMixin, UserAuditMixin


class User(Base, TimeStampMixin, UserAuditMixin):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid4
    )
    username: Mapped[str] = mapped_column(Unicode(32), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(Unicode(320), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Unicode(128), nullable=False)
    full_name: Mapped[str] = mapped_column(Unicode(128), nullable=True)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    profile_image: Mapped[str] = mapped_column(Unicode(128), nullable=True)
    last_login: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, default=func.now()
    )

    def __str__(self):
        return f"uuid: {self.uuid}, username: {self.username}, email: {self.email}"

    def __repr__(self):
        return self.__str__()
