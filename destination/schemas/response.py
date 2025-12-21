from uuid import UUID
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class AttractionDetailsResponse(BaseModel):
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


class DestinationDetailsResponse(BaseModel):
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

    attractions: List[AttractionDetailsResponse] = []
    
    is_active: bool
    is_featured: bool
    view_count: int
    
    created_at: datetime
    updated_at: datetime
