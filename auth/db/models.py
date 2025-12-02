import enum, uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column, Enum, String, DateTime, Boolean, Float, JSON
)
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base

class AccountType(str, enum.Enum):
    REGULAR = "regular"
    ADMIN = "admin"
    STAFF = "staff"

class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Basic Profile
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    profile_image_url = Column(String)

    # Localization
    language = Column(String, default="en")     # i.e. "en", "bn"
    timezone = Column(String, default="UTC")

    # Travel Preferences
    travel_style = Column(JSON)                 # ["relaxed", "adventure", "luxary"]
    budget_level = Column(String)               # low / medium / high
    prefered_group = Column(JSON)               # ["solo", "couple", "family", "friends"]
    food_preferences = Column(JSON)             # ["halal", "vegan"]
    interests = Column(JSON)                    # ["museums", "nature", "beach", "hiking"]

    # Live Location (optional)
    location_sharing_enabled = Column(Boolean, default=False)
    current_lat = Column(Float)
    current_lng = Column(Float)
    last_active_at = Column(DateTime(timezone=True))

    # Account / Security
    email_verified = Column(Boolean, default=False)
    account_type = Column(
        Enum(AccountType, native_enum=False),
        default=AccountType.REGULAR,
        nullable=False
    )

    # Admin Utility
    is_flagged = Column(Boolean, default=False)
    notes = Column(String)

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    last_login_at = Column(DateTime(timezone=True))

    is_active = Column(Boolean, default=True)