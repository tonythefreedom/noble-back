# 노블스토리지 리뷰 앱 백엔드 API

노블스토리지 이사&보관후기 앱을 위한 FastAPI 기반 백엔드 API입니다.

## 🚀 주요 기능

- **사용자 인증**: JWT 토큰 기반 관리자 인증
- **리뷰 관리**: CRUD 기능 (생성, 조회, 수정, 삭제)
- **이미지 관리**: 다중 이미지 업로드 및 관리
- **페이지네이션**: 효율적인 데이터 조회
- **보안**: 비밀번호 해싱, 토큰 인증

## 📋 API 엔드포인트

### 인증 API
- `POST /api/auth/login` - 관리자 로그인
- `POST /api/auth/logout` - 로그아웃
- `GET /api/auth/verify` - 토큰 검증

### 리뷰 API
- `GET /api/reviews` - 리뷰 목록 조회 (페이지네이션)
- `GET /api/reviews/{id}` - 특정 리뷰 상세 조회
- `POST /api/reviews` - 새 리뷰 생성 (관리자 전용)
- `PUT /api/reviews/{id}` - 리뷰 수정 (관리자 전용)
- `DELETE /api/reviews/{id}` - 리뷰 삭제 (관리자 전용)

### 이미지 API
- `POST /api/images/upload` - 이미지 업로드 (관리자 전용)
- `DELETE /api/images/{filename}` - 이미지 삭제 (관리자 전용)
- `PUT /api/reviews/{id}/images` - 리뷰 이미지 수정 (관리자 전용)

## 🛠️ 기술 스택

- **FastAPI**: 웹 프레임워크
- **SQLAlchemy**: ORM
- **SQLite**: 데이터베이스
- **JWT**: 인증
- **Pillow**: 이미지 처리
- **Pydantic**: 데이터 검증

## 📦 설치 및 실행

### 1. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 데이터베이스 초기화
```bash
python init_database.py
```

### 4. 서버 실행
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🔐 기본 계정

- **사용자명**: `tony`
- **비밀번호**: `test0723`

## 📚 API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 프로젝트 구조

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 앱
│   ├── config.py            # 설정
│   ├── database.py          # 데이터베이스 설정
│   ├── models/              # SQLAlchemy 모델
│   │   ├── user.py
│   │   ├── review.py
│   │   └── image.py
│   ├── schemas/             # Pydantic 스키마
│   │   ├── user.py
│   │   ├── review.py
│   │   └── auth.py
│   ├── api/                 # API 라우터
│   │   ├── auth.py
│   │   ├── reviews.py
│   │   └── images.py
│   ├── core/                # 핵심 기능
│   │   └── security.py
│   └── utils/               # 유틸리티
│       └── file_handler.py
├── uploads/                 # 업로드된 파일
├── database/                # 데이터베이스 파일
│   └── reviews.db
├── init_database.py         # 데이터베이스 초기화
├── requirements.txt         # 의존성
└── README.md
```

## 🔧 환경 설정

`.env` 파일을 생성하여 환경 변수를 설정할 수 있습니다:

```env
# 데이터베이스
DATABASE_URL=sqlite:///./database/reviews.db

# JWT 설정
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# 파일 업로드
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=5242880
ALLOWED_FILE_TYPES=image/jpeg,image/png,image/gif,image/webp

# 서버 설정
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

## 🧪 테스트

### cURL 예시

```bash
# 관리자 로그인
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "tony", "password": "test0723"}'

# 리뷰 목록 조회
curl -X GET "http://localhost:8000/api/reviews?page=1&limit=6"

# 특정 리뷰 조회
curl -X GET http://localhost:8000/api/reviews/1
```

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
