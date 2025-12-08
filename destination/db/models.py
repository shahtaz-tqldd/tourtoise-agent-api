import enum
import uuid
from datetime import datetime, timezone

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

class DietaryEnum(str, enum.Enum):
    VEGETARIAN = "Vegetarian"
    HALAL = "Halal"
    VEGAN = "Vegan"


# ===============================================
# REFERENCE TABLES (Reusable across destinations)
# ===============================================

class AccommodationTypeRef(Base):
    """Reference table for accommodation categories (reusable)"""
    __tablename__ = "accommodation_type_refs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)  # "Hotels", "Resorts", "Hostels"
    description = Column(Text)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    # Relationship to destination-specific instances
    destination_types = relationship("DestinationAccommodationType", back_populates="type_ref")


class TransportTypeRef(Base):
    """Reference table for transport types (reusable)"""
    __tablename__ = "transport_type_refs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)  # "CNG/Auto-rickshaw", "Taxi", "Bus"
    description = Column(Text)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    # Relationship to destination-specific instances
    destination_transports = relationship("DestinationTransportOption", back_populates="transport_ref")


class ActivityTypeRef(Base):
    """Reference table for activity types (reusable)"""
    __tablename__ = "activity_type_refs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)  # "Surfing", "Hiking", "Snorkeling"
    description = Column(Text)
    category = Column(String(100))  # "Water Sports", "Adventure", "Cultural"
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    # Relationship to destination-specific instances
    destination_activities = relationship("DestinationActivity", back_populates="activity_ref")


class DishRef(Base):
    """Reference table for signature dishes (reusable)"""
    __tablename__ = "dish_refs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)  # "Hilsa Curry", "Prawn Malai Curry"
    description = Column(Text)
    tags = Column(ARRAY(String(50)))  # ['Seafood', 'Spicy', 'Local Specialty']
    dietary_info = Column(
        ARRAY(Enum(DietaryEnum, name="dietary_enum"))
    )
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    # Relationship to destination-specific instances
    destination_dishes = relationship("DestinationSignatureDish", back_populates="dish_ref")


# ====================================
# DESTINATION-SPECIFIC JUNCTION TABLES
# ====================================

class DestinationAccommodationType(Base):
    """Links destinations to accommodation types with destination-specific details"""
    __tablename__ = "destination_accommodation_types"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    destination_id = Column(UUID(as_uuid=True), ForeignKey("destinations.id", ondelete="CASCADE"), nullable=False, index=True)
    type_ref_id = Column(UUID(as_uuid=True), ForeignKey("accommodation_type_refs.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Destination-specific details
    price_range = Column(String(100), nullable=False)  # "1,500 - 8,000 BDT/night" (varies by destination)
    description = Column(Text)  # Optional destination-specific notes
    availability = Column(String(100))  # "Year-round", "Seasonal"
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    destination = relationship("Destination", back_populates="accommodation_types")
    type_ref = relationship("AccommodationTypeRef", back_populates="destination_types")


class DestinationTransportOption(Base):
    """Links destinations to transport types with destination-specific details"""
    __tablename__ = "destination_transport_options"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    destination_id = Column(UUID(as_uuid=True), ForeignKey("destinations.id", ondelete="CASCADE"), nullable=False, index=True)
    transport_ref_id = Column(UUID(as_uuid=True), ForeignKey("transport_type_refs.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Destination-specific details
    price_range = Column(String(100), nullable=False)  # "100 - 300 BDT" (varies by destination)
    description = Column(Text)  # Local tips, availability notes
    availability = Column(String(100))  # "24/7", "6 AM - 10 PM"
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    destination = relationship("Destination", back_populates="transportation_options")
    transport_ref = relationship("TransportTypeRef", back_populates="destination_transports")


class DestinationActivity(Base):
    """Links destinations to activities with destination-specific details"""
    __tablename__ = "destination_activities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    destination_id = Column(UUID(as_uuid=True), ForeignKey("destinations.id", ondelete="CASCADE"), nullable=False, index=True)
    activity_ref_id = Column(UUID(as_uuid=True), ForeignKey("activity_type_refs.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Destination-specific details
    price_range = Column(String(100))  # "500 - 1,500 BDT" (varies by destination)
    description = Column(Text)  # Destination-specific details
    duration = Column(String(100))  # "2-3 hours"
    difficulty = Column(String(50))  # "Easy", "Moderate", "Difficult"
    best_season = Column(String(100))
    booking_required = Column(Boolean, default=False)
    is_popular = Column(Boolean, default=False, index=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    destination = relationship("Destination", back_populates="activities")
    activity_ref = relationship("ActivityTypeRef", back_populates="destination_activities")


class DestinationSignatureDish(Base):
    """Links destinations to dishes with destination-specific details"""
    __tablename__ = "destination_signature_dishes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    destination_id = Column(UUID(as_uuid=True), ForeignKey("destinations.id", ondelete="CASCADE"), nullable=False, index=True)
    dish_ref_id = Column(UUID(as_uuid=True), ForeignKey("dish_refs.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Destination-specific details
    price_range = Column(String(100))  # "200-500 BDT" (varies by destination)
    is_recommended = Column(Boolean, default=False, index=True)
    local_notes = Column(Text)  # Special preparation or serving style in this destination
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    destination = relationship("Destination", back_populates="signature_dishes")
    dish_ref = relationship("DishRef", back_populates="destination_dishes")


# ======================
# MAIN DESTINATION TABLE
# ======================

class Destination(Base):
    __tablename__ = "destinations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic Info
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    tags = Column(ARRAY(String(50)))
    
    # Highlights
    best_time = Column(String(255))
    cost_level = Column(Enum(CostLevel), index=True)
    avg_duration = Column(String(100))
    suitable_for = Column(ARRAY(String(50)))
    popular_for = Column(ARRAY(String(50)))

    # Location
    country = Column(String(100), nullable=False, index=True)
    region = Column(String(255), nullable=False, index=True)
    longitude = Column(DECIMAL(10, 7))
    latitude = Column(DECIMAL(10, 7))
    timezone = Column(String(50), default="UTC")

    # Visit Info
    weather = Column(Text)
    peak_season = Column(String(255))
    festivals = Column(Text)

    # Practical Info
    languages = Column(ARRAY(String(50)))
    payment_methods = Column(ARRAY(String(50)))
    safety_tips = Column(Text)
    customs = Column(Text)
    how_to_reach = Column(Text)
    
    # Meta
    is_active = Column(Boolean, default=True, index=True)
    is_featured = Column(Boolean, default=False, index=True)
    view_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships - Reference-based (many-to-many through junction tables)
    accommodation_types = relationship("DestinationAccommodationType", back_populates="destination", cascade="all, delete-orphan")
    transportation_options = relationship("DestinationTransportOption", back_populates="destination", cascade="all, delete-orphan")
    activities = relationship("DestinationActivity", back_populates="destination", cascade="all, delete-orphan")
    signature_dishes = relationship("DestinationSignatureDish", back_populates="destination", cascade="all, delete-orphan")
    
    # Relationships - Destination-specific entities
    images = relationship("DestinationImage", back_populates="destination", cascade="all, delete-orphan")
    accommodations = relationship("Accommodation", back_populates="destination", cascade="all, delete-orphan")
    attractions = relationship("Attraction", back_populates="destination", cascade="all, delete-orphan")
    restaurants = relationship("Restaurant", back_populates="destination", cascade="all, delete-orphan")


# =============================
# DESTINATION-SPECIFIC ENTITIES
# =============================

class DestinationImage(Base):
    __tablename__ = "destination_images"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    destination_id = Column(UUID(as_uuid=True), ForeignKey("destinations.id", ondelete="CASCADE"), nullable=False, index=True)
    
    image_url = Column(String(500), nullable=False)
    alt_text = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    destination = relationship("Destination", back_populates="images")


class Accommodation(Base):
    """Specific accommodation properties (bound to destination)"""
    __tablename__ = "accommodations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    destination_id = Column(UUID(as_uuid=True), ForeignKey("destinations.id", ondelete="CASCADE"), nullable=False, index=True)
    accommodation_type_id = Column(UUID(as_uuid=True), ForeignKey("destination_accommodation_types.id", ondelete="SET NULL"), nullable=True, index=True)
    
    name = Column(String(255), nullable=False)
    price_range = Column(String(100), nullable=False)
    rating = Column(DECIMAL(3, 2))
    
    # Location
    distance = Column(String(100))
    region = Column(String(255), nullable=False, index=True)
    longitude = Column(DECIMAL(10, 7))
    latitude = Column(DECIMAL(10, 7))
    
    # Contact
    phone = Column(String(20))
    email = Column(String(100))
    website = Column(String(255))
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    destination = relationship("Destination", back_populates="accommodations")
    accommodation_type = relationship("DestinationAccommodationType")


class Attraction(Base):
    """Tourist attractions (bound to destination)"""
    __tablename__ = "attractions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    destination_id = Column(UUID(as_uuid=True), ForeignKey("destinations.id", ondelete="CASCADE"), nullable=False, index=True)
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    image_url = Column(String(500))
    tag = Column(Enum(AttractionTag), index=True)
    
    entry_fee = Column(String(100))
    opening_hours = Column(String(255))
    best_time_to_visit = Column(String(255))
    available_transports = Column(ARRAY(String(50)))
    is_recommended = Column(Boolean, default=False, index=True)
    
    # Location
    region = Column(String(255), nullable=False, index=True)
    longitude = Column(DECIMAL(10, 7))
    latitude = Column(DECIMAL(10, 7))
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    destination = relationship("Destination", back_populates="attractions")


class Restaurant(Base):
    """Restaurants (bound to destination)"""
    __tablename__ = "restaurants"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    destination_id = Column(UUID(as_uuid=True), ForeignKey("destinations.id", ondelete="CASCADE"), nullable=False, index=True)
    
    name = Column(String(255), nullable=False)
    rating = Column(DECIMAL(3, 2))
    price_range = Column(String(100))
    
    signature_dishes = Column(ARRAY(String(100)))
    cuisine_type = Column(ARRAY(String(50)))
    contact = Column(String(50))
    opening_hours = Column(String(255))
    accepts_reservation = Column(Boolean, default=False)
    is_recommended = Column(Boolean, default=False, index=True)
    
    # Location
    region = Column(String(255), nullable=False, index=True)
    longitude = Column(DECIMAL(10, 7))
    latitude = Column(DECIMAL(10, 7))

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    destination = relationship("Destination", back_populates="restaurants")