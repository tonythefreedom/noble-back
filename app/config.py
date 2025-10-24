from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # 데이터베이스
    database_url: str = "sqlite:///./database/reviews.db"
    
    # JWT 설정
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    
    # 파일 업로드
    upload_dir: str = "./uploads"
    max_file_size: int = 5242880  # 5MB
    allowed_file_types: List[str] = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    
    # 서버 설정
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# 전역 설정 인스턴스
settings = Settings()

# 업로드 디렉토리 생성
os.makedirs(settings.upload_dir, exist_ok=True)
os.makedirs("database", exist_ok=True)
