from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api import auth, reviews, images
from app.database import engine
from app.models import User, Review, ReviewImage, AdminSession
from app.config import settings

import os

# FastAPI 앱 생성
app = FastAPI(
    title="노블스토리지 리뷰 API",
    description="노블스토리지 이사&보관후기 앱을 위한 백엔드 API",
    version="1.0.0"
)

# CORS 설정 (로컬 테스트 포트 포함, 프로덕션 도메인 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://noblestorage.co.kr",
        "https://www.noblestorage.co.kr",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "*",
        "Authorization",
        "If-Modified-Since",
        "Cache-Control",
        "Content-Type",
        "Range"
    ],
    expose_headers=["Content-Length", "Content-Range"]
)

# 항상 JSON 응답을 보장하는 예외 핸들러 (API 경로에 한함)
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if request.url.path.startswith("/api/"):
        return JSONResponse({"success": False, "detail": exc.detail}, status_code=exc.status_code)
    return JSONResponse({"error": exc.detail}, status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if request.url.path.startswith("/api/"):
        return JSONResponse({"success": False, "detail": exc.errors()}, status_code=422)
    return JSONResponse({"error": exc.errors()}, status_code=422)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    if request.url.path.startswith("/api/"):
        return JSONResponse({"success": False, "detail": "internal server error"}, status_code=500)
    return JSONResponse({"error": "internal server error"}, status_code=500)

# 정적 파일 서빙 (업로드된 이미지)
_uploads_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads"))
app.mount("/uploads", StaticFiles(directory=_uploads_dir), name="uploads")

# API 라우터 등록
app.include_router(auth.router, prefix="/api/auth", tags=["인증"])
app.include_router(reviews.router, prefix="/api", tags=["리뷰"])
app.include_router(images.router, prefix="/api", tags=["이미지"])

@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행"""
    # 데이터베이스 테이블 생성
    from app.database import Base
    Base.metadata.create_all(bind=engine)
    
    # 기본 관리자 계정 생성
    from app.database import SessionLocal
    from app.models.user import User as UserModel
    from app.core.security import get_password_hash
    
    db = SessionLocal()
    try:
        admin_user = db.query(UserModel).filter(UserModel.username == "tony").first()
        if not admin_user:
            admin_user = UserModel(
                username="tony",
                password_hash=get_password_hash("test0723"),
                role="admin"
            )
            db.add(admin_user)
            db.commit()
            print("기본 관리자 계정이 생성되었습니다: tony / test0723")
    finally:
        db.close()

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "노블스토리지 리뷰 API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )