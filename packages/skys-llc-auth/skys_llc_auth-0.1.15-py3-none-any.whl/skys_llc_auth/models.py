import uuid
from datetime import datetime
from typing import TypeVar

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

T = TypeVar("T", bound="CredentialStorage")


class Base(DeclarativeBase): ...


class CredentialStorage(Base):
    __abstract__ = True

    @declared_attr  # pyright: ignore[reportArgumentType]
    @classmethod
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    access_token: Mapped[str] = mapped_column(String(2500), nullable=True)
    refresh_token: Mapped[str] = mapped_column(String(2500), nullable=True)
    login: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    access_until: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    service_name: Mapped[str] = mapped_column(nullable=True)
