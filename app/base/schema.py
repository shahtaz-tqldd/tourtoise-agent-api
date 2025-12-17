from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel, Field, model_validator

DataT = TypeVar("DataT")


class BaseResponse(BaseModel):
    """Base response schema"""
    success: bool = Field(default=True, description="Request success status")
    message: str = Field(default="Success", description="Response message")


class DataResponse(BaseResponse, Generic[DataT]):
    """Response with data payload"""
    data: DataT = Field(..., description="Response data")


class ListMeta(BaseModel):
    total: int = Field(default=0, description="Total count of items")
    page: int = Field(default=1, ge=1, description="Current page number")
    page_size: int = Field(default=50, ge=1, le=100, description="Items per page")
    total_pages: int = Field(default=0, description="Total number of pages")

class ListResponse(BaseResponse, Generic[DataT]):
    data: List[DataT] = Field(default_factory=list)

    # incoming fields (not exposed)
    total: int = Field(exclude=True)
    page: int = Field(exclude=True)
    page_size: int = Field(exclude=True)

    # outgoing meta
    meta: ListMeta | None = None

    @model_validator(mode="after")
    def build_meta(self):
        total_pages = (
            (self.total + self.page_size - 1) // self.page_size
            if self.page_size > 0
            else 0
        )

        self.meta = ListMeta(
            total=self.total,
            page=self.page,
            page_size=self.page_size,
            total_pages=total_pages,
        )
        return self


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