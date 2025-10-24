from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.user import User
from app.api.auth import get_current_admin_user
from app.utils.file_handler import save_uploaded_file, get_file_url, delete_file
import os

router = APIRouter()

@router.post("/images/upload")
async def upload_image(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """이미지 업로드 (관리자 전용)"""
    try:
        filename = save_uploaded_file(image)
        return {
            "success": True,
            "data": {
                "image_url": get_file_url(filename),
                "filename": filename,
                "size": image.size,
                "mime_type": image.content_type
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"이미지 업로드 실패: {str(e)}"
        )

@router.delete("/images/{filename}")
async def delete_image(
    filename: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """이미지 삭제 (관리자 전용)"""
    success = delete_file(filename)
    
    if success:
        return {
            "success": True,
            "message": "이미지가 성공적으로 삭제되었습니다."
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="이미지를 찾을 수 없습니다."
        )

@router.put("/reviews/{review_id}/images")
async def update_review_images(
    review_id: int,
    images: List[UploadFile] = File(...),
    remove_images: Optional[List[int]] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """리뷰 이미지 수정 (관리자 전용)"""
    from app.models.review import Review
    from app.models.image import ReviewImage
    
    review = db.query(Review).filter(Review.id == review_id).first()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="리뷰를 찾을 수 없습니다."
        )
    
    # 기존 이미지 삭제
    removed_images = []
    if remove_images:
        for img_id in remove_images:
            img = db.query(ReviewImage).filter(ReviewImage.id == img_id).first()
            if img:
                delete_file(img.image_filename)
                db.delete(img)
                removed_images.append(img_id)
    
    # 새 이미지 추가
    added_images = []
    if images:
        saved_files = []
        for file in images:
            filename = save_uploaded_file(file)
            saved_files.append(filename)
        
        for i, filename in enumerate(saved_files):
            review_image = ReviewImage(
                review_id=review.id,
                image_url=get_file_url(filename),
                image_filename=filename,
                sort_order=len(review.images) + i
            )
            db.add(review_image)
            added_images.append({
                "id": review_image.id,
                "image_url": get_file_url(filename),
                "sort_order": review_image.sort_order
            })
    
    db.commit()
    
    return {
        "success": True,
        "message": "리뷰 이미지가 성공적으로 수정되었습니다.",
        "data": {
            "added_images": added_images,
            "removed_images": removed_images
        }
    }
