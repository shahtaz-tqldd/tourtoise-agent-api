from uuid import UUID
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class AttractionImageDetails(BaseModel):
    """Attraction image details"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    image_url: str
    alt_text: Optional[str] = None


class DestinationImageDetails(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    image_url: str
    alt_text: Optional[str] = None


class AttractionDetails(BaseModel):
    """Attraction response with images"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    description: Optional[str] = ""
    tag: Optional[str] = ""
    entry_fee: Optional[str] = ""
    opening_hours: Optional[str] = ""
    is_recommended: Optional[bool] = False
    region: Optional[str] = ""
    best_time_to_visit: Optional[str] = ""
    available_transports: Optional[List[str]] = []
    longitude: Optional[Decimal] = None
    latitude: Optional[Decimal] = None
    images: List[AttractionImageDetails] = []


class AccommodationTypeRefDetails(BaseModel):
    """Details from the accommodation_type_refs table"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    description: Optional[str] = None


class AccommodationTypeDetails(BaseModel):
    """Destination-specific accommodation type with reference details"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    price_range: str
    availability: Optional[str] = None
    description: Optional[str] = None
    type_ref: AccommodationTypeRefDetails  # This is the relationship to get the name


class AccommodationTypeForAccommodation(BaseModel):
    """Simplified accommodation type for accommodation response"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    price_range: str
    type_ref: AccommodationTypeRefDetails


class AccommodationDetails(BaseModel):
    """Accommodation with type name"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    price_range: str
    rating: Optional[Decimal] = None
    distance: Optional[str] = None
    region: Optional[str] = None
    longitude: Optional[Decimal] = None
    latitude: Optional[Decimal] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    accommodation_type: Optional[AccommodationTypeForAccommodation] = None


class TransportRefDetails(BaseModel):
    """Details from the transport_type_refs table"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    description: Optional[str] = None


class TransportOptionDetails(BaseModel):
    """Transport option with reference details"""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    price_range: str
    availability: Optional[str] = None
    description: Optional[str] = None
    transport_ref: TransportRefDetails  # This is the relationship to get the name


class ActivityRefDetails(BaseModel):
    """Details from the activity_type_refs table"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    description: Optional[str] = None
    category: Optional[str] = None


class ActivityDetails(BaseModel):
    """Destination-specific activity with reference details"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    price_range: Optional[str] = None
    duration: Optional[str] = None
    best_season: Optional[str] = None
    booking_required: bool = False
    is_popular: bool = False
    description: Optional[str] = None
    activity_ref: ActivityRefDetails  # This is the relationship to get the name


class SignatureDishResponse(BaseModel):
    """Signature dish response"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    tags: List[str] = []
    dietary_info: List[str] = []
    price_range: Optional[str] = None
    is_recommended: bool = False
    local_notes: Optional[str] = None


class DestinationBasicDetails(BaseModel):
    """Basic destination details for response"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    slug: str
    name: str
    description: Optional[str]
    tags: List[str]
    images: List[DestinationImageDetails] = []

    best_time: Optional[str]
    cost_level: Optional[str]
    avg_duration: Optional[str]

    country: str
    region: str


class DestinationDetails(BaseModel):
    """Complete destination details response schema"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    description: Optional[str]
    tags: List[str] = []
    
    best_time: Optional[str]
    cost_level: Optional[str]
    avg_duration: Optional[str]
    
    suitable_for: List[str] = []
    popular_for: List[str] = []
    
    country: str
    region: str
    longitude: Optional[Decimal]
    latitude: Optional[Decimal]
    timezone: Optional[str]
    
    weather: Optional[str]
    peak_season: Optional[str]
    festivals: Optional[str]
    
    languages: List[str] = []
    payment_methods: List[str] = []
    
    safety_tips: Optional[str]
    customs: Optional[str]
    how_to_reach: Optional[str]

    attractions: List[AttractionDetails] = []
    
    is_active: bool
    is_featured: bool
    view_count: int
    
    created_at: datetime
    updated_at: datetime


# Full Destination Details
class DestinationFullDetails(BaseModel):
    """Complete destination details with all relationships"""
    model_config = ConfigDict(from_attributes=True)
    
    slug: str
    name: str
    description: Optional[str]
    tags: List[str] = []
    
    best_time: Optional[str]
    cost_level: Optional[str]
    avg_duration: Optional[str]
    
    suitable_for: List[str] = []
    popular_for: List[str] = []
    
    country: str
    region: str
    longitude: Optional[Decimal]
    latitude: Optional[Decimal]
    timezone: Optional[str]
    
    weather: Optional[str]
    peak_season: Optional[str]
    festivals: Optional[str]
    
    languages: List[str] = []
    payment_methods: List[str] = []
    
    safety_tips: Optional[str]
    customs: Optional[str]
    how_to_reach: Optional[str]
    
    is_active: bool
    is_featured: bool
    view_count: int
    
    created_at: datetime
    updated_at: datetime
    
    # Related entities with names from reference tables
    images: List[DestinationImageDetails] = []
    attractions: List[AttractionDetails] = []
    transportation_options: List[TransportOptionDetails] = []
    signature_dishes: List[SignatureDishResponse] = []
    accommodation_types: List[AccommodationTypeDetails] = []
    accommodations: List[AccommodationDetails] = []
    activities: List[ActivityDetails] = []