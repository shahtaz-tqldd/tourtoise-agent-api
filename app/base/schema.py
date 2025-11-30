from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel, Field

DataT = TypeVar("DataT")


class BaseResponse(BaseModel):
    """Base response schema"""
    success: bool = Field(default=True, description="Request success status")
    message: str = Field(default="Success", description="Response message")


class DataResponse(BaseResponse, Generic[DataT]):
    """Response with data payload"""
    data: DataT = Field(..., description="Response data")


class ListResponse(BaseResponse, Generic[DataT]):
    """Response for list endpoints with pagination"""
    data: List[DataT] = Field(default_factory=list, description="List of items")
    total: int = Field(default=0, description="Total count of items")
    page: int = Field(default=1, ge=1, description="Current page number")
    page_size: int = Field(default=50, ge=1, le=100, description="Items per page")
    
    @property
    def total_pages(self) -> int:
        """Calculate total number of pages"""
        if self.page_size == 0:
            return 0
        return (self.total + self.page_size - 1) // self.page_size


class ErrorDetail(BaseModel):
    """Error detail schema"""
    field: str
    message: str
    type: str


class ErrorResponse(BaseModel):
    """Error response schema"""
    success: bool = Field(default=False)
    status_code: int
    message: str
    error_type: str
    errors: Optional[List[ErrorDetail]] = None
    details: Optional[dict] = None


class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int