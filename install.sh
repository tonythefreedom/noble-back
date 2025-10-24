#!/bin/bash

# Noble Storage Review App - 백엔드 자동 설치 스크립트
# Ubuntu/Debian 환경용

set -e  # 에러 발생 시 스크립트 중단

echo "🚀 Noble Storage Review App 백엔드 설치를 시작합니다..."

# 1. 시스템 업데이트
echo "📦 시스템 패키지 업데이트 중..."
sudo apt update && sudo apt upgrade -y

# 2. 필수 패키지 설치
echo "🔧 필수 패키지 설치 중..."
sudo apt install -y python3.12 python3.12-venv python3.12-dev python3-pip nginx git curl

# 3. 프로젝트 디렉토리 생성
echo "📁 프로젝트 디렉토리 설정 중..."
PROJECT_DIR="/opt/noble-back"
sudo mkdir -p $PROJECT_DIR
sudo chown $USER:$USER $PROJECT_DIR

# 4. 프로젝트 클론 (GitHub에서)
echo "📥 프로젝트 코드 다운로드 중..."
cd $PROJECT_DIR
git clone https://github.com/tonythefreedom/noble-back.git .

# 5. Python 가상환경 설정
echo "🐍 Python 가상환경 설정 중..."
python3.12 -m venv venv
source venv/bin/activate

# 6. 의존성 설치
echo "📚 Python 패키지 설치 중..."
pip install --upgrade pip
pip install -r requirements.txt

# 7. 데이터베이스 초기화
echo "🗄️ 데이터베이스 초기화 중..."
python init_database.py

# 8. Nginx 설정
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

# 9. Nginx 사이트 활성화
echo "🔗 Nginx 사이트 활성화 중..."
sudo ln -sf /etc/nginx/sites-available/noble-back /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# 10. Nginx 설정 테스트 및 재시작
echo "✅ Nginx 설정 테스트 중..."
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx

# 11. 시스템 서비스 설정
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

# 12. 서비스 시작
echo "🚀 서비스 시작 중..."
sudo systemctl daemon-reload
sudo systemctl enable noble-back
sudo systemctl start noble-back

# 13. 방화벽 설정
echo "🔥 방화벽 설정 중..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# 14. 설치 완료 확인
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
