from uuid import UUID
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict


from pydantic import BaseModel
from typing import List, Optional, Any


class AccommodationTypeRequest(BaseModel):
    name: str
    description: Optional[str]

class AccommodationTypeDetails(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    description: Optional[str]
    
# class AccommodationTypeRequest(BaseModel):
#     accommodation_type_ref_id: str
#     price_range: str
#     availability: str
#     description: Optional[str]


class TransportOptionRequest(BaseModel):
    transport_type_ref_id: str
    price_range: str
    availability: str
    description: Optional[str]


class ActivityRequest(BaseModel):
    activity_type_ref_id: str
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
    accommodation_type_ref_id: str
    price_range: str
    rating: Optional[str]
    distance: Optional[str]
    region: Optional[str]
    longitude: Optional[str]
    latitude: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    website: Optional[str]


class AttractionRequest(BaseModel):
    name: str
    description: Optional[str]
    image_file: Optional[Any]
    tag: Optional[str]
    entry_fee: Optional[str]
    opening_hours: Optional[str]
    best_time_to_visit: Optional[str]
    available_transports: List[str] = []
    is_recommended: bool
    region: Optional[str]
    longitude: Optional[str]
    latitude: Optional[str]


class ImageRequest(BaseModel):
    file: Any
    alt_text: Optional[str]


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
    """destination specific details"""
    model_config = ConfigDict(from_attributes=True)
    name: str

    

class ShortDestinationDetails(BaseModel):
    """destination specific details"""
    model_config = ConfigDict(from_attributes=True)

    name: str

    

