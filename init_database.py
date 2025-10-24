#!/usr/bin/env python3
"""
데이터베이스 초기화 및 더미 데이터 생성 스크립트
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.user import User
from app.models.review import Review
from app.models.image import ReviewImage
from app.core.security import get_password_hash
from app.database import Base
import random
from datetime import datetime, timedelta

def init_database():
    """데이터베이스 초기화"""
    # 테이블 생성
    Base.metadata.create_all(bind=engine)
    print("데이터베이스 테이블이 생성되었습니다.")

def create_admin_user():
    """관리자 계정 생성"""
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.username == "tony").first()
        if not admin_user:
            admin_user = User(
                username="tony",
                password_hash=get_password_hash("test0723"),
                role="admin"
            )
            db.add(admin_user)
            db.commit()
            print("관리자 계정이 생성되었습니다: tony / test0723")
        else:
            print("관리자 계정이 이미 존재합니다.")
    finally:
        db.close()

def create_dummy_reviews():
    """더미 리뷰 데이터 생성 (설치 시에는 생성하지 않음)"""
    print("설치 시에는 더미 리뷰 데이터를 생성하지 않습니다.")
    print("관리자 계정으로 로그인하여 리뷰를 직접 작성하세요.")

def main():
    """메인 실행 함수"""
    print("데이터베이스 초기화를 시작합니다...")
    
    # 데이터베이스 초기화
    init_database()
    
    # 관리자 계정 생성
    create_admin_user()
    
    # 더미 데이터 생성
    create_dummy_reviews()
    
    print("데이터베이스 초기화가 완료되었습니다!")

if __name__ == "__main__":
    main()
