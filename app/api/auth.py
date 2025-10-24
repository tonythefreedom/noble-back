from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse, LogoutResponse, VerifyResponse
from app.core.security import verify_password, create_access_token, verify_token
from datetime import timedelta
from app.config import settings

router = APIRouter()
security = HTTPBearer()

@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """관리자 로그인"""
    user = db.query(User).filter(User.username == login_data.username).first()
    
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 사용자명 또는 비밀번호입니다."
        )
    
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="관리자 권한이 필요합니다."
        )
    
    # JWT 토큰 생성
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id, "role": user.role},
        expires_delta=access_token_expires
    )
    
    return LoginResponse(
        success=True,
        message="로그인 성공",
        data={
            "token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role
            }
        }
    )

@router.post("/logout", response_model=LogoutResponse)
async def logout():
    """로그아웃"""
    return LogoutResponse(
        success=True,
        message="로그아웃 성공"
    )

@router.get("/verify", response_model=VerifyResponse)
async def verify_token_endpoint(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """토큰 검증"""
    payload = verify_token(credentials.credentials)
    
    return VerifyResponse(
        success=True,
        data={
            "user": {
                "username": payload.get("sub"),
                "user_id": payload.get("user_id"),
                "role": payload.get("role")
            }
        }
    )

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    """현재 사용자 정보 가져오기"""
    payload = verify_token(credentials.credentials)
    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없습니다."
        )
    
    return user

def get_current_admin_user(current_user: User = Depends(get_current_user)):
    """현재 관리자 사용자 확인"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="관리자 권한이 필요합니다."
        )
    return current_user
