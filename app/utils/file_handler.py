import os
import uuid
from typing import List
from fastapi import UploadFile, HTTPException, status
from app.config import settings
from PIL import Image

def validate_image_file(file: UploadFile) -> bool:
    """이미지 파일 유효성 검사"""
    if file.content_type not in settings.allowed_file_types:
        return False
    
    if file.size and file.size > settings.max_file_size:
        return False
    
    return True

def save_uploaded_file(file: UploadFile) -> str:
    """업로드된 파일 저장"""
    if not validate_image_file(file):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type or size"
        )
    
    # 고유한 파일명 생성
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.upload_dir, unique_filename)
    
    # 파일 저장
    with open(file_path, "wb") as buffer:
        content = file.file.read()
        buffer.write(content)
    
    return unique_filename

def save_multiple_files(files: List[UploadFile]) -> List[str]:
    """여러 파일 저장"""
    saved_files = []
    for file in files:
        if validate_image_file(file):
            filename = save_uploaded_file(file)
            saved_files.append(filename)
    
    return saved_files

def delete_file(filename: str) -> bool:
    """파일 삭제"""
    file_path = os.path.join(settings.upload_dir, filename)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception:
        return False

def get_file_url(filename: str) -> str:
    """파일 URL 생성"""
    return f"/uploads/{filename}"

def resize_image(file_path: str, max_size: tuple = (800, 600)) -> str:
    """이미지 리사이징"""
    try:
        with Image.open(file_path) as img:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            img.save(file_path, optimize=True, quality=85)
        return file_path
    except Exception:
        return file_path
