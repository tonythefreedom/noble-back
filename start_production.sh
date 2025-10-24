#!/bin/bash

# 프로덕션 환경 실행 스크립트
# Gunicorn을 사용하여 여러 워커로 FastAPI 실행

echo "🚀 Noble Storage Review App - 프로덕션 서버 시작"
echo "📊 워커 수: 4개"
echo "🌐 포트: 8000"
echo "⚡ 워커 타입: UvicornWorker"

# 가상환경 활성화
source venv/bin/activate

# Gunicorn으로 프로덕션 서버 실행
exec gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --timeout 120 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 100
