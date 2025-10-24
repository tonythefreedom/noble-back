# 🚀 Noble Storage Review App - 프로덕션 배포 가이드

## 📋 개요

이 문서는 Noble Storage Review App 백엔드를 프로덕션 환경에 배포하기 위한 설정 가이드입니다.

## ⚠️ FastAPI 단독 사용의 문제점

### 성능 및 확장성
- 단일 프로세스로 실행되어 동시 요청 처리 제한
- 로드 밸런싱 어려움
- 메모리 사용량 최적화 부족

### 보안 문제
- 직접적인 HTTP 서버로 보안 헤더 부족
- SSL/TLS 종료 처리 복잡
- 정적 파일 서빙 시 보안 취약점

### 운영 관리
- 로그 관리 및 모니터링 어려움
- 프로세스 관리 및 재시작 복잡
- 헬스체크 및 장애 복구 어려움

## 🏗️ 권장 프로덕션 아키텍처

### 1. 소규모 프로젝트 (권장)
```
Internet → Nginx → Gunicorn + FastAPI
```

### 2. 중대형 프로젝트
```
Internet → Load Balancer → Nginx → Gunicorn + FastAPI (Multiple Instances)
```

### 3. 클라우드 배포
```
Internet → Cloud Load Balancer → Kubernetes → Docker Containers (FastAPI)
```

## 🛠️ 프로덕션 설정

### 1. 의존성 설치

```bash
# 가상환경 활성화
source venv/bin/activate

# 프로덕션 의존성 설치
pip install gunicorn
```

### 2. Gunicorn 설정

#### 기본 실행
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### 고급 설정
```bash
gunicorn app.main:app \
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
```

### 3. 프로덕션 실행 스크립트

`start_production.sh` 파일을 사용하여 프로덕션 서버를 시작할 수 있습니다:

```bash
# 실행 권한 부여
chmod +x start_production.sh

# 프로덕션 서버 시작
./start_production.sh
```

## 🔧 Nginx 설정 (권장)

### 1. Nginx 설치 확인

#### Nginx 설치 위치 확인
```bash
# Nginx 실행 파일 위치 확인
which nginx
# 출력 예시: /usr/sbin/nginx

# Nginx 실행 파일 상세 정보
whereis nginx
# 출력 예시: nginx: /usr/sbin/nginx /usr/lib/nginx /etc/nginx /usr/share/nginx

# Nginx 설정 파일 위치 확인
nginx -T 2>/dev/null | grep "configuration file"
# 출력 예시: configuration file /etc/nginx/nginx.conf

# Nginx 프로세스 확인
ps aux | grep nginx
# 출력 예시:
# root      1234  0.0  0.0  12345  1234 ?        Ss   10:00   0:00 nginx: master process /usr/sbin/nginx
# www-data  1235  0.0  0.0  12345  1234 ?        S    10:00   0:00 nginx: worker process
```

#### Nginx 디렉토리 구조 확인
```bash
# Nginx 설정 디렉토리 확인
ls -la /etc/nginx/
# 출력 예시:
# drwxr-xr-x 2 root root 4096 Oct 24 10:00 conf.d
# drwxr-xr-x 2 root root 4096 Oct 24 10:00 sites-available
# drwxr-xr-x 2 root root 4096 Oct 24 10:00 sites-enabled
# -rw-r--r-- 1 root root 1234 Oct 24 10:00 nginx.conf

# 사이트 설정 디렉토리 확인
ls -la /etc/nginx/sites-available/
ls -la /etc/nginx/sites-enabled/

# 로그 디렉토리 확인
ls -la /var/log/nginx/
# 출력 예시:
# -rw-r--r-- 1 www-data adm 1234 Oct 24 10:00 access.log
# -rw-r--r-- 1 www-data adm 1234 Oct 24 10:00 error.log
```

#### Nginx 기본 설정 확인
```bash
# Nginx 버전 및 모듈 정보
nginx -V
# 출력 예시:
# nginx version: nginx/1.18.0 (Ubuntu)
# built by gcc 9.3.0 (Ubuntu 9.3.0-10ubuntu2)
# configure arguments: --with-cc-opt='-g -O2 -fdebug-prefix-map=/build/nginx-1.18.0=. -fstack-protector-strong -Wformat -Werror=format-security -fPIC -Wdate-time -D_FORTIFY_SOURCE=2' --with-ld-opt='-Wl,-Bsymbolic-functions -Wl,-z,relro -Wl,-z,now -fPIC' --prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --http-client-body-temp-path=/var/cache/nginx/client_temp --http-proxy-temp-path=/var/cache/nginx/proxy_temp --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp --http-scgi-temp-path=/var/cache/nginx/scgi_temp --with-perl_modules_path=/usr/lib/perl5/vendor_perl --user=www-data --group=www-data --with-compat --with-file-aio --with-threads --with-http_addition_module --with-http_auth_request_module --with-http_dav_module --with-http_flv_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module --with-http_random_index_module --with-http_realip_module --with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module --with-http_v2_module --with-mail --with-mail_ssl_module --with-stream --with-stream_realip_module --with-stream_ssl_module --with-stream_ssl_preread_module

# Nginx 설정 파일 문법 검사
sudo nginx -t
# 성공 시 출력:
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# nginx: configuration file /etc/nginx/nginx.conf test is successful
```

#### Nginx 상태 및 서비스 확인
```bash
# Nginx 버전 확인
nginx -v
# 출력 예시: nginx version: nginx/1.18.0 (Ubuntu)

# Nginx 상태 확인
sudo systemctl status nginx
# 출력 예시:
# ● nginx.service - A high performance web server and a reverse proxy server
#      Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
#      Active: active (running) since Thu 2024-10-24 10:00:00 KST; 1h 30min ago
#        Docs: man:nginx(8)
#    Main PID: 1234 (nginx)
#       Tasks: 2 (limit: 4915)
#      Memory: 2.5M
#      CGroup: /system.slice/nginx.service
#              ├─1234 nginx: master process /usr/sbin/nginx -g daemon on; master_process on;
#              └─1235 nginx: worker process

# Nginx 시작 (필요시)
sudo systemctl start nginx

# Nginx 자동 시작 설정
sudo systemctl enable nginx

# Nginx 재시작
sudo systemctl restart nginx

# Nginx 리로드 (설정 변경 후)
sudo systemctl reload nginx
```

#### Nginx 포트 및 네트워크 확인
```bash
# Nginx가 사용하는 포트 확인
sudo netstat -tlnp | grep nginx
# 출력 예시:
# tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      1234/nginx: master
# tcp        0      0 0.0.0.0:443             0.0.0.0:*               LISTEN      1234/nginx: master

# 또는 ss 명령어 사용
sudo ss -tlnp | grep nginx

# 방화벽 상태 확인 (Ubuntu/Debian)
sudo ufw status
# 출력 예시:
# Status: active
# To                         Action      From
# --                         ------      ----
# 22/tcp                     ALLOW       Anywhere
# 80/tcp                     ALLOW       Anywhere
# 443/tcp                    ALLOW       Anywhere
```

### 2. Nginx 설정 파일 생성

#### 사이트별 설정 파일 생성
```bash
# 사이트 설정 파일 생성
sudo nano /etc/nginx/sites-available/noble-back

# 심볼릭 링크 생성 (활성화)
sudo ln -s /etc/nginx/sites-available/noble-back /etc/nginx/sites-enabled/

# 기본 설정 파일 비활성화 (필요시)
sudo rm /etc/nginx/sites-enabled/default
```

### 3. Nginx 설정 파일 내용

#### /etc/nginx/sites-available/noble-back
```nginx
# 업스트림 서버 정의 (로드 밸런싱)
upstream fastapi_backend {
    server 127.0.0.1:8000 weight=3;
    server 127.0.0.1:8001 weight=1 backup;  # 백업 서버
    keepalive 32;
}

# HTTP 서버 설정
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # 로그 설정
    access_log /var/log/nginx/noble-back.access.log;
    error_log /var/log/nginx/noble-back.error.log;
    
    # 보안 헤더
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # 클라이언트 최대 업로드 크기
    client_max_body_size 10M;
    
    # API 프록시 설정
    location /api/ {
        proxy_pass http://fastapi_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $server_name;
        
        # 타임아웃 설정
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # 버퍼링 설정
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
        
        # CORS 헤더 (필요시)
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
        add_header Access-Control-Allow-Headers "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization";
        
        # OPTIONS 요청 처리
        if ($request_method = 'OPTIONS') {
            add_header Access-Control-Allow-Origin *;
            add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
            add_header Access-Control-Allow-Headers "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization";
            add_header Access-Control-Max-Age 1728000;
            add_header Content-Type 'text/plain; charset=utf-8';
            add_header Content-Length 0;
            return 204;
        }
    }
    
    # 정적 파일 서빙 (업로드된 이미지)
    location /uploads/ {
        alias /path/to/your/app/uploads/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header X-Content-Type-Options nosniff;
        
        # 이미지 최적화
        location ~* \.(jpg|jpeg|png|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
    
    # 헬스체크 엔드포인트
    location /health {
        proxy_pass http://fastapi_backend;
        access_log off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # 루트 경로 (프론트엔드가 별도 서버인 경우)
    location / {
        return 301 https://your-frontend-domain.com$request_uri;
    }
    
    # 보안 설정
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    # robots.txt
    location = /robots.txt {
        allow all;
        log_not_found off;
        access_log off;
    }
}
```

### 4. Nginx 설정 적용 및 테스트

#### 설정 파일 문법 검사
```bash
# Nginx 설정 파일 문법 검사
sudo nginx -t

# 성공 시 출력 예시:
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# nginx: configuration file /etc/nginx/nginx.conf test is successful
```

#### Nginx 재시작
```bash
# Nginx 재시작
sudo systemctl restart nginx

# Nginx 상태 확인
sudo systemctl status nginx

# Nginx 로그 확인
sudo tail -f /var/log/nginx/noble-back.access.log
sudo tail -f /var/log/nginx/noble-back.error.log
```

#### 설정 테스트
```bash
# API 엔드포인트 테스트
curl -I http://your-domain.com/api/reviews

# 헬스체크 테스트
curl http://your-domain.com/health

# 정적 파일 테스트
curl -I http://your-domain.com/uploads/test-image.jpg
```

### 5. SSL 인증서 설정 (Let's Encrypt)

#### Certbot 설치
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install certbot python3-certbot-nginx

# CentOS/RHEL
sudo yum install certbot python3-certbot-nginx
```

#### SSL 인증서 발급
```bash
# 도메인에 SSL 인증서 발급
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 자동 갱신 설정
sudo crontab -e
# 다음 라인 추가:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

#### HTTPS 리다이렉트 설정
```nginx
# HTTP에서 HTTPS로 리다이렉트
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS 서버 설정
server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;
    
    # SSL 인증서 설정
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # SSL 보안 설정
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # HSTS 헤더
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # 기존 설정들...
}
```

### 6. Nginx 성능 최적화

#### /etc/nginx/nginx.conf 최적화
```nginx
# 메인 nginx.conf 파일에 추가
worker_processes auto;
worker_cpu_affinity auto;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    # 기본 설정
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    
    # Gzip 압축
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;
    
    # 버퍼 크기 최적화
    client_body_buffer_size 128k;
    client_max_body_size 10m;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 4k;
    
    # 타임아웃 설정
    client_body_timeout 12;
    client_header_timeout 12;
    keepalive_timeout 15;
    send_timeout 10;
}
```

### 7. 모니터링 및 로그 관리

#### 로그 로테이션 설정
```bash
# /etc/logrotate.d/nginx 파일 생성
sudo nano /etc/logrotate.d/nginx

# 내용:
/var/log/nginx/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 640 nginx adm
    sharedscripts
    postrotate
        if [ -f /var/run/nginx.pid ]; then
            kill -USR1 `cat /var/run/nginx.pid`
        fi
    endscript
}
```

#### 실시간 모니터링
```bash
# 실시간 접근 로그 모니터링
sudo tail -f /var/log/nginx/noble-back.access.log

# 에러 로그 모니터링
sudo tail -f /var/log/nginx/noble-back.error.log

# Nginx 상태 모니터링
curl http://localhost/nginx_status
```

## 🐳 Docker 설정

### Dockerfile
```dockerfile
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 포트 노출
EXPOSE 8000

# 프로덕션 서버 실행
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./database/reviews.db
    volumes:
      - ./uploads:/app/uploads
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - app
    restart: unless-stopped
```

## 📊 성능 비교

| 구성 | 동시 사용자 | 응답 시간 | 안정성 | 권장도 |
|------|------------|----------|--------|--------|
| FastAPI 단독 | ~100 | 빠름 | 낮음 | ❌ |
| Gunicorn + FastAPI | ~500+ | 빠름 | 중간 | ✅ |
| Nginx + Gunicorn + FastAPI | ~1000+ | 빠름 | 높음 | ✅✅ |
| Docker + Kubernetes | ~10000+ | 빠름 | 매우 높음 | ✅✅✅ |

## 🔍 모니터링 및 로그

### 1. 로그 설정
```python
# app/main.py에 추가
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 2. 헬스체크 엔드포인트
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}
```

### 3. 시스템 모니터링
```bash
# 프로세스 모니터링
ps aux | grep gunicorn

# 포트 모니터링
netstat -tlnp | grep 8000

# 로그 모니터링
tail -f /var/log/nginx/access.log
```

## 🚀 배포 체크리스트

### 배포 전 확인사항
- [ ] 데이터베이스 백업 완료
- [ ] 환경 변수 설정 확인
- [ ] SSL 인증서 설정 (프로덕션)
- [ ] 방화벽 설정 확인
- [ ] 로그 디렉토리 권한 확인

### 배포 후 확인사항
- [ ] API 엔드포인트 정상 작동
- [ ] 정적 파일 서빙 확인
- [ ] 로그 파일 생성 확인
- [ ] 헬스체크 엔드포인트 확인
- [ ] 성능 테스트 완료

## 📞 문제 해결

### 일반적인 문제들

1. **포트 충돌**
   ```bash
   # 포트 사용 확인
   lsof -i :8000
   ```

2. **권한 문제**
   ```bash
   # 실행 권한 부여
   chmod +x start_production.sh
   ```

3. **메모리 부족**
   ```bash
   # 워커 수 조정
   gunicorn app.main:app -w 2  # 워커 수 감소
   ```

## 📚 추가 리소스

- [Gunicorn 공식 문서](https://docs.gunicorn.org/)
- [Nginx 설정 가이드](https://nginx.org/en/docs/)
- [FastAPI 배포 가이드](https://fastapi.tiangolo.com/deployment/)
- [Docker 베스트 프랙티스](https://docs.docker.com/develop/best-practices/)

---

**⚠️ 중요**: 프로덕션 환경에서는 반드시 Nginx 프록시를 사용하고, SSL 인증서를 설정하여 보안을 강화하세요.
