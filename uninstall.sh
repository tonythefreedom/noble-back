#!/bin/bash

# Noble Storage Review App - 완전 제거 스크립트
# Ubuntu/Debian 환경용

set -e  # 에러 발생 시 스크립트 중단

echo "🗑️ Noble Storage Review App 완전 제거를 시작합니다..."

# 1. 서비스 중지 및 비활성화
echo "🛑 서비스 중지 중..."
sudo systemctl stop noble-back 2>/dev/null || true
sudo systemctl disable noble-back 2>/dev/null || true

# 2. 서비스 파일 삭제
echo "📄 서비스 파일 삭제 중..."
sudo rm -f /etc/systemd/system/noble-back.service
sudo systemctl daemon-reload

# 3. Nginx 설정 삭제
echo "🌐 Nginx 설정 삭제 중..."
sudo rm -f /etc/nginx/sites-enabled/noble-back
sudo rm -f /etc/nginx/sites-available/noble-back
sudo systemctl reload nginx

# 4. 프로젝트 디렉토리 삭제
echo "📁 프로젝트 디렉토리 삭제 중..."
PROJECT_DIR="/opt/noble-back"
if [ -d "$PROJECT_DIR" ]; then
    sudo rm -rf $PROJECT_DIR
    echo "✅ 프로젝트 디렉토리 삭제 완료: $PROJECT_DIR"
else
    echo "⚠️ 프로젝트 디렉토리가 존재하지 않습니다: $PROJECT_DIR"
fi

# 5. 로그 파일 삭제
echo "📝 로그 파일 삭제 중..."
sudo rm -f /var/log/nginx/noble-back.access.log
sudo rm -f /var/log/nginx/noble-back.error.log

# 6. 방화벽 규칙 제거 (선택사항)
echo "🔥 방화벽 규칙 확인 중..."
if sudo ufw status | grep -q "80/tcp"; then
    echo "⚠️ 방화벽 규칙이 남아있습니다. 수동으로 제거하세요:"
    echo "   sudo ufw delete allow 80/tcp"
    echo "   sudo ufw delete allow 443/tcp"
fi

# 7. Python 패키지 정리 (선택사항)
echo "🐍 Python 패키지 정리 중..."
echo "⚠️ Python 패키지는 수동으로 정리하세요:"
echo "   - 가상환경: $PROJECT_DIR/venv (이미 삭제됨)"
echo "   - 시스템 Python 패키지: pip freeze > requirements_backup.txt"
echo "   - 불필요한 패키지 제거: pip uninstall -r requirements.txt"

# 8. 완료 확인
echo ""
echo "🎉 Noble Storage Review App 제거가 완료되었습니다!"
echo ""
echo "📋 제거된 항목:"
echo "   - 서비스: noble-back"
echo "   - 프로젝트 디렉토리: $PROJECT_DIR"
echo "   - Nginx 설정: /etc/nginx/sites-*/noble-back"
echo "   - 로그 파일: /var/log/nginx/noble-back.*"
echo ""
echo "🔧 수동 정리가 필요한 항목:"
echo "   - 방화벽 규칙 (필요시)"
echo "   - Python 패키지 (필요시)"
echo "   - SSL 인증서 (필요시)"
echo ""
echo "🚀 다시 설치하려면:"
echo "   curl -O https://raw.githubusercontent.com/tonythefreedom/noble-back/main/install.sh"
echo "   chmod +x install.sh"
echo "   ./install.sh"
