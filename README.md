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

## 🚀 프로덕션 배포 스크립트

### 백엔드 애플리케이션 자동 설치 스크립트

#### 1. 전체 설치 스크립트 (install.sh)
```bash
#!/bin/bash

# Noble Storage Review App - 백엔드 자동 설치 스크립트
# Ubuntu/Debian 환경용

set -e  # 에러 발생 시 스크립트 중단

echo "🚀 Noble Storage Review App 백엔드 설치를 시작합니다..."

# 1. 시스템 업데이트
echo "📦 시스템 패키지 업데이트 중..."
sudo apt update && sudo apt upgrade -y

# 2. Python 3.12 설치 (deadsnakes PPA 사용)
echo "🐍 Python 3.12 설치 중..."
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-dev python3.12-distutils

# 3. pip 설치
echo "📦 pip 설치 중..."
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12

# 4. 필수 패키지 설치
echo "🔧 필수 패키지 설치 중..."
sudo apt install -y nginx git curl build-essential

# 5. 프로젝트 디렉토리 생성
echo "📁 프로젝트 디렉토리 설정 중..."
PROJECT_DIR="/opt/noble-back"
sudo mkdir -p $PROJECT_DIR
sudo chown $USER:$USER $PROJECT_DIR

# 6. 프로젝트 클론 (GitHub에서)
echo "📥 프로젝트 코드 다운로드 중..."
cd $PROJECT_DIR
git clone https://github.com/tonythefreedom/noble-back.git .

# 7. Python 가상환경 설정
echo "🐍 Python 가상환경 설정 중..."
python3.12 -m venv venv
source venv/bin/activate

# 8. 의존성 설치
echo "📚 Python 패키지 설치 중..."
pip install --upgrade pip
pip install -r requirements.txt

# 9. 데이터베이스 초기화
echo "🗄️ 데이터베이스 초기화 중..."
python init_database.py

# 10. Nginx 설정
echo "🌐 Nginx 설정 중..."
sudo tee /etc/nginx/sites-available/noble-back > /dev/null <<EOF
upstream fastapi_backend {
    server 127.0.0.1:8000;
    keepalive 32;
}

server {
    listen 80;
    server_name _;
    
    # 로그 설정
    access_log /var/log/nginx/noble-back.access.log;
    error_log /var/log/nginx/noble-back.error.log;
    
    # 보안 헤더
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    
    # API 프록시
    location /api/ {
        proxy_pass http://fastapi_backend;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # CORS 헤더
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
        add_header Access-Control-Allow-Headers "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization";
    }
    
    # 정적 파일 서빙
    location /uploads/ {
        alias $PROJECT_DIR/uploads/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # 헬스체크
    location /health {
        proxy_pass http://fastapi_backend;
        access_log off;
    }
}
EOF

# 11. Nginx 사이트 활성화
echo "🔗 Nginx 사이트 활성화 중..."
sudo ln -sf /etc/nginx/sites-available/noble-back /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# 12. Nginx 설정 테스트 및 재시작
echo "✅ Nginx 설정 테스트 중..."
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx

# 13. 시스템 서비스 설정
echo "⚙️ 시스템 서비스 설정 중..."
sudo tee /etc/systemd/system/noble-back.service > /dev/null <<EOF
[Unit]
Description=Noble Storage Review App Backend
After=network.target

[Service]
Type=exec
User=$USER
Group=$USER
WorkingDirectory=$PROJECT_DIR
Environment=PATH=$PROJECT_DIR/venv/bin
ExecStart=$PROJECT_DIR/venv/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# 14. 서비스 시작
echo "🚀 서비스 시작 중..."
sudo systemctl daemon-reload
sudo systemctl enable noble-back
sudo systemctl start noble-back

# 15. 방화벽 설정
echo "🔥 방화벽 설정 중..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# 16. 설치 완료 확인
echo "✅ 설치 완료 확인 중..."
sleep 5

# 서비스 상태 확인
if sudo systemctl is-active --quiet noble-back; then
    echo "✅ Noble Back 서비스가 정상적으로 실행 중입니다."
else
    echo "❌ Noble Back 서비스 시작에 실패했습니다."
    sudo systemctl status noble-back
    exit 1
fi

# Nginx 상태 확인
if sudo systemctl is-active --quiet nginx; then
    echo "✅ Nginx가 정상적으로 실행 중입니다."
else
    echo "❌ Nginx 시작에 실패했습니다."
    sudo systemctl status nginx
    exit 1
fi

# API 테스트
echo "🧪 API 연결 테스트 중..."
if curl -s http://localhost/api/health > /dev/null; then
    echo "✅ API가 정상적으로 응답합니다."
else
    echo "⚠️ API 연결 테스트에 실패했습니다. 서비스 로그를 확인하세요."
fi

echo ""
echo "🎉 Noble Storage Review App 백엔드 설치가 완료되었습니다!"
echo ""
echo "📋 설치 정보:"
echo "   - 프로젝트 경로: $PROJECT_DIR"
echo "   - 서비스 이름: noble-back"
echo "   - API 엔드포인트: http://your-server-ip/api/"
echo "   - 헬스체크: http://your-server-ip/health"
echo ""
echo "🔧 관리 명령어:"
echo "   - 서비스 상태: sudo systemctl status noble-back"
echo "   - 서비스 재시작: sudo systemctl restart noble-back"
echo "   - 로그 확인: sudo journalctl -u noble-back -f"
echo "   - Nginx 재시작: sudo systemctl restart nginx"
echo ""
echo "📚 자세한 설정은 prod.md 파일을 참고하세요."
```

#### 2. 설치 스크립트 실행
```bash
# 스크립트 다운로드 및 실행
curl -O https://raw.githubusercontent.com/tonythefreedom/noble-back/main/install.sh
chmod +x install.sh
sudo ./install.sh
```

#### 3. 수동 설치 (단계별)
```bash
# 1. 필수 패키지 설치
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-dev python3-pip nginx git

# 2. 프로젝트 클론
git clone https://github.com/tonythefreedom/noble-back.git /opt/noble-back
cd /opt/noble-back

# 3. 가상환경 설정
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. 데이터베이스 초기화
python init_database.py

# 5. Nginx 설정
sudo cp nginx.conf /etc/nginx/sites-available/noble-back
sudo ln -s /etc/nginx/sites-available/noble-back /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx

# 6. 서비스 등록
sudo cp noble-back.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable noble-back
sudo systemctl start noble-back
```

#### 4. 설치 후 확인
```bash
# 서비스 상태 확인
sudo systemctl status noble-back
sudo systemctl status nginx

# API 테스트
curl http://localhost/api/health
curl http://localhost/api/reviews?page=1&limit=3

# 로그 확인
sudo journalctl -u noble-back -f
sudo tail -f /var/log/nginx/noble-back.access.log
```

#### 5. 문제 해결
```bash
# 서비스 재시작
sudo systemctl restart noble-back
sudo systemctl restart nginx

# 설정 파일 문법 검사
sudo nginx -t

# 포트 사용 확인
sudo netstat -tlnp | grep :8000
sudo netstat -tlnp | grep :80

# 권한 확인
ls -la /opt/noble-back/
sudo chown -R $USER:$USER /opt/noble-back/
```

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
