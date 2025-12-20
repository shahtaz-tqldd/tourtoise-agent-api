from datetime import datetime
from decimal import Decimal
from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Any
from uuid import UUID


class AccommodationTypeRequest(BaseModel):
    name: str
    description: Optional[str] = None

class AccommodationTypeDetails(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    description: Optional[str]


class TransportTypeRequest(BaseModel):
    name: str
    description: Optional[str] = None

class TransportTypeDetails(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    description: Optional[str]

class ActivityTypeRequest(BaseModel):
    name: str
    description: Optional[str] = None

class ActivityTypeDetails(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    description: Optional[str]
    
class AccommodationTypeRequest(BaseModel):
    accommodation_type_id: str
    price_range: str
    availability: str
    description: Optional[str]


class TransportOptionRequest(BaseModel):
    transport_type_id: str
    price_range: str
    availability: str
    description: Optional[str]


class ActivityRequest(BaseModel):
    activity_type_id: str
    price_range: str
    duration: str
    best_season: str
    booking_required: bool
    is_popular: bool
    description: Optional[str]


class SignatureDishRequest(BaseModel):
    name: str
    tags: Optional[str]
    dietary_info: Optional[str]
    price_range: str
    is_recommended: bool
    local_notes: Optional[str]


class AccommodationRequest(BaseModel):
    name: str
    accommodation_type_id: str
    price_range: str
    rating: Optional[str]
    distance: Optional[str]
    region: Optional[str]
    longitude: Optional[str]
    latitude: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    website: Optional[str]


class ImageRequest(BaseModel):
    file: UploadFile
    alt_text: Optional[str] = None


class AttractionRequest(BaseModel):
    name: str
    description: Optional[str]
    image_file: ImageRequest
    tag: Optional[str]
    entry_fee: Optional[str]
    opening_hours: Optional[str]
    best_time_to_visit: Optional[str]
    available_transports: List[str] = []
    is_recommended: bool
    region: Optional[str]
    longitude: Optional[str]
    latitude: Optional[str]

class DestinationCreateRequest(BaseModel):
    """destination creation request schema"""

    name: str
    description: Optional[str]
    tags: List[str]

    best_time: Optional[str]
    cost_level: Optional[str]
    avg_duration: Optional[str]

    suitable_for: List[str]
    popular_for: List[str]

    country: str
    region: str
    longitude: str
    latitude: str
    timezone: Optional[str]

    weather: Optional[str]
    peak_season: Optional[str]
    festivals: Optional[str]

    languages: List[str]
    payment_methods: List[str]

    safety_tips: Optional[str]
    customs: Optional[str]
    how_to_reach: Optional[str]

    accommodation_types: List[AccommodationTypeRequest]
    transport_options: List[TransportOptionRequest]
    activities: List[ActivityRequest]
    signature_dishes: List[SignatureDishRequest]

    accommodations: List[AccommodationRequest]
    attractions: List[AttractionRequest]
    images: List[ImageRequest]


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
    
    is_active: bool
    is_featured: bool
    view_count: int
    
    created_at: datetime
    updated_at: datetime


class DestinationFullDetails(BaseModel):
    """Complete destination details with all relationships"""
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
    
    is_active: bool
    is_featured: bool
    view_count: int
    
    created_at: datetime
    updated_at: datetime
    
    # Related entities counts or summaries
    accommodation_types_count: int = 0
    transport_options_count: int = 0
    activities_count: int = 0
    signature_dishes_count: int = 0
    accommodations_count: int = 0
    attractions_count: int = 0
    images_count: int = 0

    

class DestinationBasicDetails(BaseModel):
    """Basic destination details for response"""
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    description: Optional[str]
    tags: List[str]

    best_time: Optional[str]
    cost_level: Optional[str]
    avg_duration: Optional[str]

    country: str
    region: str


class AccommodationTypeResponse(BaseModel):
    """Accommodation type response"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    type_ref_id: UUID
    price_range: str
    availability: Optional[str]
    description: Optional[str]


class TransportOptionResponse(BaseModel):
    """Transport option response"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    transport_ref_id: UUID
    price_range: str
    availability: Optional[str]
    description: Optional[str]


class ActivityResponse(BaseModel):
    """Activity response"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    activity_ref_id: UUID
    price_range: Optional[str]
    duration: Optional[str]
    best_season: Optional[str]
    booking_required: bool
    is_popular: bool
    description: Optional[str]


class SignatureDishResponse(BaseModel):
    """Signature dish response"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    tags: List[str] = []
    dietary_info: List[str] = []
    price_range: Optional[str]
    is_recommended: bool
    local_notes: Optional[str]


class AccommodationResponse(BaseModel):
    """Accommodation response"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    price_range: str
    rating: Optional[Decimal]
    region: str
    phone: Optional[str]
    email: Optional[str]
    website: Optional[str]


class AttractionResponse(BaseModel):
    """Attraction response"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    description: Optional[str]
    tag: Optional[str]
    entry_fee: Optional[str]
    opening_hours: Optional[str]
    is_recommended: bool
    region: str

