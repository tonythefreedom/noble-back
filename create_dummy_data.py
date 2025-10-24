#!/usr/bin/env python3
"""
더미 리뷰 데이터 생성 스크립트
개발 및 테스트용
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.models.review import Review
from app.models.image import ReviewImage
import random
from datetime import datetime, timedelta

def create_dummy_reviews():
    """더미 리뷰 데이터 생성"""
    print("더미 리뷰 데이터 생성을 시작합니다...")
    
    db = SessionLocal()
    try:
        # 기존 더미 데이터가 있는지 확인
        existing_reviews = db.query(Review).count()
        if existing_reviews > 0:
            print(f"이미 {existing_reviews}개의 리뷰가 존재합니다.")
            return
        
        # 관리자 사용자 가져오기
        admin_user = db.query(User).filter(User.username == "tony").first()
        if not admin_user:
            print("관리자 사용자를 찾을 수 없습니다.")
            return
        
        # 더미 데이터 생성
        teams = ["27팀", "15팀", "32팀", "8팀", "41팀", "19팀", "23팀", "36팀", "12팀", "45팀"]
        locations = [
            ("경기 군포시", "서울 노원구"),
            ("서울 강남구", "서울 서초구"),
            ("경기 성남시", "서울 송파구"),
            ("인천 연수구", "서울 마포구"),
            ("경기 수원시", "서울 영등포구"),
            ("서울 강동구", "서울 중랑구"),
            ("경기 안양시", "서울 도봉구"),
            ("서울 금천구", "서울 강서구"),
            ("경기 의정부시", "서울 동대문구"),
            ("서울 종로구", "서울 중구")
        ]
        
        contents = [
            "정말 친절하게 도와주셨어요. 이사가 생각보다 편했어요.",
            "팀원분들이 정말 세심하게 챙겨주셔서 감사했습니다.",
            "빠르고 안전하게 이사 완료했습니다. 추천해요!",
            "가격도 합리적이고 서비스도 훌륭했습니다.",
            "이사 전 걱정이 많았는데 덕분에 안심하고 이사할 수 있었어요.",
            "정말 만족스러운 서비스였습니다. 감사합니다!",
            "친절하고 전문적인 서비스에 감동받았습니다.",
            "이사 준비부터 완료까지 모든 과정이 완벽했습니다.",
            "다음에도 꼭 이용하고 싶은 업체입니다.",
            "정말 추천하고 싶은 이사 업체입니다."
        ]
        
        for i in range(50):
            team = random.choice(teams)
            from_loc, to_loc = random.choice(locations)
            content = random.choice(contents)
            
            # 날짜 생성 (최근 30일 내)
            days_ago = random.randint(1, 30)
            from_date = (datetime.now() - timedelta(days=days_ago)).strftime("%m.%d")
            to_date = (datetime.now() - timedelta(days=days_ago-1)).strftime("%m.%d")
            
            review = Review(
                user_id=admin_user.id,
                team=team,
                title=f"{team} {i+1}차 후기입니다~",
                content=content,
                from_location=from_loc,
                to_location=to_loc,
                from_date=from_date,
                to_date=to_date,
                rating=random.randint(4, 5),  # 4-5점
                status="published"
            )
            
            db.add(review)
            db.flush()  # ID를 얻기 위해 flush
            
            # 더미 이미지 생성 (1-3개)
            num_images = random.randint(1, 3)
            for j in range(num_images):
                # 더미 이미지 URL (실제로는 picsum.photos 사용)
                image_url = f"https://picsum.photos/800/600?random={i*10+j}"
                filename = f"review_{review.id}_{j+1}.jpg"
                
                review_image = ReviewImage(
                    review_id=review.id,
                    image_url=image_url,
                    image_filename=filename,
                    sort_order=j
                )
                db.add(review_image)
        
        db.commit()
        print("✅ 50개의 더미 리뷰 데이터가 생성되었습니다.")
        
    except Exception as e:
        print(f"❌ 더미 데이터 생성 중 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_dummy_reviews()
