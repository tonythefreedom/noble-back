from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ReviewImageBase(BaseModel):
    image_url: str
    sort_order: int = 0

class ReviewImageCreate(ReviewImageBase):
    pass

class ReviewImage(ReviewImageBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    team: str
    title: str
    content: str
    from_location: str
    to_location: str
    from_date: str
    to_date: str
    rating: int = Field(..., ge=1, le=5)
    status: str = "published"

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    team: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    from_location: Optional[str] = None
    to_location: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[str] = None

class ReviewInDB(ReviewBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Review(ReviewInDB):
    images: List[ReviewImage] = []
    user_name: Optional[str] = None
    # 프론트엔드 호환성을 위한 추가 필드
    userName: Optional[str] = None
    date: Optional[str] = None
    image: Optional[str] = None
    # 추가 필드들
    images_detail: Optional[List[dict]] = None

class ReviewList(BaseModel):
    reviews: List[Review]
    pagination: dict

class ReviewResponse(BaseModel):
    success: bool = True
    data: Review

class ReviewListResponse(BaseModel):
    success: bool = True
    data: ReviewList
