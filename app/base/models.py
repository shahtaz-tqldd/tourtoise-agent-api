from datetime import datetime
from typing import Optional

from sqlalchemy.orm import declared_attr, Mapped, mapped_column
from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase


class TimestampMixin:
    """Adds created_at, updated_at timestamp fields to models."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


class UserTrackMixin:
    """Adds created_by / updated_by fields (simple string or FK later)."""

    created_by: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    updated_by: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )


# Combine into one base mixin for convenience
class BaseModel(DeclarativeBase, TimestampMixin, UserTrackMixin):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
