from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, Form, File
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from app.database import get_db
from app.models.user import User
from app.models.review import Review
from app.models.image import ReviewImage
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse, ReviewListResponse
from app.api.auth import get_current_admin_user
from app.utils.file_handler import save_multiple_files, get_file_url, delete_file
from math import ceil

router = APIRouter()

@router.get("/reviews")
async def get_reviews(
    page: int = Query(1, ge=1),
    limit: int = Query(6, ge=1, le=50),
    status_filter: str = Query("published", alias="status"),
    db: Session = Depends(get_db)
):
    """리뷰 목록 조회 (페이지네이션)"""
    # 총 개수 계산
    total_count = db.query(Review).filter(Review.status == status_filter).count()
    
    # 페이지네이션 계산
    total_pages = ceil(total_count / limit)
    offset = (page - 1) * limit
    
    # 리뷰 조회
    reviews = db.query(Review).filter(Review.status == status_filter)\
        .order_by(desc(Review.created_at))\
        .offset(offset).limit(limit).all()
    
    # 리뷰 데이터 변환
    review_list = []
    for review in reviews:
        # 이미지 URL 생성
        images = []
        for img in review.images:
            images.append({
                "id": img.id,
                "image_url": get_file_url(img.image_filename),
                "sort_order": img.sort_order
            })
        
        # 메인 이미지 (첫 번째 이미지)
        main_image = images[0]["image_url"] if images else ""
        
        review_data = {
            "id": review.id,
            "user_id": review.user_id,
            "team": review.team,
            "title": review.title,
            "content": review.content,
            "from_location": review.from_location,
            "to_location": review.to_location,
            "from_date": review.from_date,
            "to_date": review.to_date,
            "rating": review.rating,
            "status": review.status,
            "created_at": review.created_at,
            "updated_at": review.updated_at,
            "userName": f"**님",  # 개인정보 보호
            "date": "2일전",  # 실제로는 created_at에서 계산
            "image": main_image,
            "images": [img["image_url"] for img in images],
            "images_detail": images
        }
        review_list.append(review_data)
    
    return {
        "success": True,
        "data": {
            "reviews": review_list,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "total_items": total_count,
                "items_per_page": limit
            }
        }
    }

@router.get("/reviews/{review_id}", response_model=ReviewResponse)
async def get_review(review_id: int, db: Session = Depends(get_db)):
    """특정 리뷰 상세 조회"""
    review = db.query(Review).filter(Review.id == review_id).first()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="리뷰를 찾을 수 없습니다."
        )
    
    # 이미지 데이터
    images = []
    for img in review.images:
        images.append({
            "id": img.id,
            "image_url": get_file_url(img.image_filename),
            "sort_order": img.sort_order
        })
    
    # 메인 이미지
    main_image = images[0]["image_url"] if images else ""
    
    review_data = {
        "id": review.id,
        "team": review.team,
        "title": review.title,
        "userName": f"**님",
        "date": "2일전",
        "fromLocation": review.from_location,
        "toLocation": review.to_location,
        "fromDate": review.from_date,
        "toDate": review.to_date,
        "rating": review.rating,
        "image": main_image,
        "images": [img["image_url"] for img in images],
        "content": review.content,
        "created_at": review.created_at,
        "images_detail": images
    }
    
    return ReviewResponse(success=True, data=review_data)

@router.post("/reviews", response_model=dict)
async def create_review(
    team: str = Form(...),
    title: str = Form(...),
    userName: str = Form(...),
    fromLocation: str = Form(...),
    toLocation: str = Form(...),
    fromDate: str = Form(...),
    toDate: str = Form(...),
    rating: int = Form(...),
    content: str = Form(...),
    images: List[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """새 리뷰 생성 (관리자 전용)"""
    # 리뷰 생성
    review = Review(
        user_id=current_user.id,
        team=team,
        title=title,
        content=content,
        from_location=fromLocation,
        to_location=toLocation,
        from_date=fromDate,
        to_date=toDate,
        rating=rating,
        status="published"
    )
    
    db.add(review)
    db.commit()
    db.refresh(review)
    
    # 이미지 처리
    if images:
        saved_files = save_multiple_files(images)
        for i, filename in enumerate(saved_files):
            review_image = ReviewImage(
                review_id=review.id,
                image_url=get_file_url(filename),
                image_filename=filename,
                sort_order=i
            )
            db.add(review_image)
    
    db.commit()
    
    return {
        "success": True,
        "message": "리뷰가 성공적으로 생성되었습니다.",
        "data": {"review_id": review.id}
    }

@router.put("/reviews/{review_id}", response_model=dict)
async def update_review(
    review_id: int,
    team: Optional[str] = None,
    title: Optional[str] = None,
    userName: Optional[str] = None,
    fromLocation: Optional[str] = None,
    toLocation: Optional[str] = None,
    fromDate: Optional[str] = None,
    toDate: Optional[str] = None,
    rating: Optional[int] = None,
    content: Optional[str] = None,
    images: List[UploadFile] = None,
    remove_existing_images: List[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """리뷰 수정 (관리자 전용)"""
    review = db.query(Review).filter(Review.id == review_id).first()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="리뷰를 찾을 수 없습니다."
        )
    
    # 필드 업데이트
    if team is not None:
        review.team = team
    if title is not None:
        review.title = title
    if fromLocation is not None:
        review.from_location = fromLocation
    if toLocation is not None:
        review.to_location = toLocation
    if fromDate is not None:
        review.from_date = fromDate
    if toDate is not None:
        review.to_date = toDate
    if rating is not None:
        review.rating = rating
    if content is not None:
        review.content = content
    
    # 기존 이미지 삭제
    if remove_existing_images:
        for img_id in remove_existing_images:
            img = db.query(ReviewImage).filter(ReviewImage.id == img_id).first()
            if img:
                delete_file(img.image_filename)
                db.delete(img)
    
    # 새 이미지 추가
    if images:
        saved_files = save_multiple_files(images)
        for i, filename in enumerate(saved_files):
            review_image = ReviewImage(
                review_id=review.id,
                image_url=get_file_url(filename),
                image_filename=filename,
                sort_order=len(review.images) + i
            )
            db.add(review_image)
    
    db.commit()
    
    return {
        "success": True,
        "message": "리뷰가 성공적으로 수정되었습니다.",
        "data": {
            "review_id": review.id,
            "updated_at": review.updated_at
        }
    }

@router.delete("/reviews/{review_id}", response_model=dict)
async def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """리뷰 삭제 (관리자 전용)"""
    review = db.query(Review).filter(Review.id == review_id).first()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="리뷰를 찾을 수 없습니다."
        )
    
    # 이미지 파일 삭제
    for img in review.images:
        delete_file(img.image_filename)
    
    db.delete(review)
    db.commit()
    
    return {
        "success": True,
        "message": "리뷰가 성공적으로 삭제되었습니다."
    }
