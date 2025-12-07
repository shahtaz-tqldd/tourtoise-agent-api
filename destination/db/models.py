import enum
import uuid
from datetime import datetime, timezone
from typing import List

from sqlalchemy import (
    Column, Enum, String, DateTime, Boolean,
    Text, Integer, DECIMAL, ForeignKey, ARRAY
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class CostLevel(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class AttractionTag(str, enum.Enum):
    NATURE = "Nature"
    HISTORIC = "Historic"
    CULTURE = "Culture"
    ADVENTURE = "Adventure"
    PHOTO_SPOT = "Photo Spot"
    RELIGIOUS = "Religious"
    BEACH = "Beach"
    SHOPPING = "Shopping"


class Destination(Base):
    __tablename__ = "destinations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic Info
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    tags = Column(ARRAY(String(50)))  # ['Beach', 'Nature', 'Budget-Friendly']
    
    # Highlights
    best_time = Column(String(255))
    cost_level = Column(Enum(CostLevel), index=True)
    avg_duration = Column(String(100))  # "2-3 days"
    suitable_for = Column(ARRAY(String(50)))  # ['Families', 'Couples', 'Solo']
    popular_for = Column(ARRAY(String(50)))  # ['Beaches', 'Sunsets', 'Seafood']

    # Location
    region = Column(String(255), nullable=False, index=True)
    country = Column(String(100), nullable=False, index=True)
    longitude = Column(DECIMAL(10, 7), nullable=False)
    latitude = Column(DECIMAL(10, 7), nullable=False)
    timezone = Column(String(50), default="UTC")

    # Visit Info
    weather = Column(Text)
    peak_season = Column(String(255))
    festivals = Column(Text)

    # Practical Info
    languages = Column(ARRAY(String(50)))
    payment_methods = Column(ARRAY(String(50)))
    safety_tips = Column(Text)  # Store as HTML or Markdown
    customs = Column(Text)  # Store as HTML or Markdown
    
    # Transportation Info (denormalized for quick access)
    how_to_reach = Column(Text)
    
    # Meta
    is_active = Column(Boolean, default=True, index=True)
    is_featured = Column(Boolean, default=False, index=True)
    view_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    images = relationship(
        "DestinationImage",
        back_populates="destination",
        cascade="all, delete-orphan"
    )
    stay_types = relationship(
        "AccommodationType",
        back_populates="destination",
        cascade="all, delete-orphan"
    )
    accommodations = relationship(
        "Accommodation",
        back_populates="destination",
        cascade="all, delete-orphan"
    )
    attractions = relationship(
        "Attraction",
        back_populates="destination",
        cascade="all, delete-orphan"
    )
    transportation_options = relationship(
        "TransportationOption",
        back_populates="destination",
        cascade="all, delete-orphan"
    )
    activities = relationship(
        "Activity",
        back_populates="destination",
        cascade="all, delete-orphan"
    )
    restaurants = relationship(
        "Restaurant",
        back_populates="destination",
        cascade="all, delete-orphan"
    )
    signature_dishes = relationship(
        "SignatureDish",
        back_populates="destination",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Destination(id={self.id}, name='{self.name}', country='{self.country}')>"



class DestinationImage(Base):
    __tablename__ = "destination_images"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    destination_id = Column(
        UUID(as_uuid=True),
        ForeignKey("destinations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    image_url = Column(String(500), nullable=False)
    alt_text = Column(String(255))
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # Relationship
    destination = relationship("Destination", back_populates="images")

    def __repr__(self):
        return f"<DestinationImage(id={self.id}, created_at={self.created_at})>"



class AccommodationType(Base):
    """Categories of accommodation (Hotels, Resorts, Hostels, etc.)"""
    __tablename__ = "accommodation_types"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    destination_id = Column(
        UUID(as_uuid=True),
        ForeignKey("destinations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    category = Column(String(100), nullable=False)  # "Hotels", "Resorts", "Hostels"
    description = Column(Text)
    price_range = Column(String(100), nullable=False)  # "1,500 - 8,000 BDT/night"
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # Relationship
    destination = relationship("Destination", back_populates="accommodation_types")

    def __repr__(self):
        return f"<AccommodationType(category='{self.category}')>"


class Accommodation(Base):
    """Specific accommodation properties (suggested stays)"""
    __tablename__ = "accommodations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    destination_id = Column(
        UUID(as_uuid=True),
        ForeignKey("destinations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    accommodation_type_id = Column(
        UUID(as_uuid=True),
        ForeignKey("accommodation_types.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    name = Column(String(255), nullable=False)
    price_range = Column(String(100), nullable=False)  # "3,500 - 6,000 BDT"
    rating = Column(DECIMAL(3, 2))  # 0.00 to 5.00
    distance = Column(String(100))  # "2 km from beach"
    
    # Optional fields
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(100))
    website = Column(String(255))
    amenities = Column(ARRAY(String(50)))  # ['WiFi', 'Pool', 'Restaurant']
    
    display_order = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)
    
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

    # Relationships
    destination = relationship("Destination", back_populates="accommodations")
    accommodation_type = relationship("AccommodationType")

    def __repr__(self):
        return f"<Accommodation(name='{self.name}', rating={self.rating})>"


class Attraction(Base):
    """Tourist attractions and points of interest"""
    __tablename__ = "attractions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    destination_id = Column(
        UUID(as_uuid=True),
        ForeignKey("destinations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    image_url = Column(String(500))
    distance = Column(String(100))  # "32 km from city center"
    tag = Column(Enum(AttractionTag), index=True)
    
    # Optional fields
    entry_fee = Column(String(100))  # "100-500 BDT" or "Free"
    opening_hours = Column(String(255))
    best_time_to_visit = Column(String(255))
    
    # Location (optional for mapping)
    longitude = Column(DECIMAL(10, 7))
    latitude = Column(DECIMAL(10, 7))
    
    # Transportation options (array of transport types available)
    available_transports = Column(ARRAY(String(50)))  # ['CNG', 'Bus', 'Private car']
    
    is_recommended = Column(Boolean, default=False, index=True)
    
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

    # Relationship
    destination = relationship("Destination", back_populates="attractions")

    def __repr__(self):
        return f"<Attraction(name='{self.name}', tag={self.tag})>"



class TransportationOption(Base):
    """Local transportation options within destination"""
    __tablename__ = "transportation_options"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    destination_id = Column(
        UUID(as_uuid=True),
        ForeignKey("destinations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    transport_type = Column(String(100), nullable=False)  # "CNG/Auto-rickshaw", "Taxi"
    description = Column(Text)  # Additional details
    price_range = Column(String(100), nullable=False)  # "100 - 300 BDT"
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # Relationship
    destination = relationship("Destination", back_populates="transportation_options")

    def __repr__(self):
        return f"<TransportationOption(type='{self.transport_type}')>"


class Activity(Base):
    """Activities and experiences available at destination"""
    __tablename__ = "activities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    destination_id = Column(
        UUID(as_uuid=True),
        ForeignKey("destinations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price_range = Column(String(100))  # "500 - 1,500 BDT"
    
    # Optional fields
    duration = Column(String(100))  # "2-3 hours"
    difficulty = Column(String(50))  # "Easy", "Moderate", "Difficult"
    best_season = Column(String(100))
    booking_required = Column(Boolean, default=False)
    
    is_popular = Column(Boolean, default=False, index=True)
    
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

    # Relationship
    destination = relationship("Destination", back_populates="activities")

    def __repr__(self):
        return f"<Activity(name='{self.name}')>"



class SignatureDish(Base):
    """Local cuisine and signature dishes"""
    __tablename__ = "signature_dishes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    destination_id = Column(
        UUID(as_uuid=True),
        ForeignKey("destinations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    tags = Column(ARRAY(String(50)))  # ['Seafood', 'Spicy', 'Local Specialty']
    is_recommended = Column(Boolean, default=False, index=True)
    
    # Optional fields
    price_range = Column(String(100))  # "200-500 BDT"
    dietary_info = Column(ARRAY(String(50)))  # ['Vegetarian', 'Halal', 'Vegan']
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # Relationship
    destination = relationship(
        "Destination",
        back_populates="signature_dishes"
    )

    def __repr__(self):
        return f"<SignatureDish(name='{self.name}')>"


class Restaurant(Base):
    """Restaurants and dining places"""
    __tablename__ = "restaurants"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    destination_id = Column(
        UUID(as_uuid=True),
        ForeignKey("destinations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    name = Column(String(255), nullable=False)
    rating = Column(DECIMAL(3, 2))  # 0.00 to 5.00
    area = Column(String(255))  # Location/neighborhood
    
    # Location
    longitude = Column(DECIMAL(10, 7))
    latitude = Column(DECIMAL(10, 7))
    
    # Menu Info
    signature_dishes = Column(ARRAY(String(100)))  # Quick reference array
    cuisine_type = Column(ARRAY(String(50)))  # ['Seafood', 'Bengali', 'Chinese']
    
    # Optional fields
    price_range = Column(String(100))  # "500-2000 BDT per person"
    phone = Column(String(20))
    opening_hours = Column(String(255))
    accepts_reservation = Column(Boolean, default=False)
    
    is_recommended = Column(Boolean, default=False, index=True)
    
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

    # Relationship
    destination = relationship(
        "Destination", 
        back_populates="restaurants"
    )

    def __repr__(self):
        return f"<Restaurant(name='{self.name}', rating={self.rating})>"
