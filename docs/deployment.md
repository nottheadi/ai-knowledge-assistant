# Deployment Guide

Complete guide for deploying the AI Knowledge Assistant to production.

---

## 🔐 Pre-Deployment Checklist

### Security

- [ ] Generate strong JWT_SECRET_KEY (min 32 chars)
- [ ] Remove default admin credentials
- [ ] Update CORS origins from `"*"` to specific domain
- [ ] Enable HTTPS only (production)
- [ ] Configure firewall rules
- [ ] Set up environment variables securely
- [ ] Review and update API rate limits
- [ ] Enable request logging and monitoring

### Configuration

- [ ] Update backend API URL in frontend environment.prod.ts
- [ ] Configure database (migrate from JSON if needed)
- [ ] Set up vector database backup strategy
- [ ] Configure file upload directory with proper permissions
- [ ] Test all API endpoints with production config
- [ ] Verify JWT token expiration settings
- [ ] Configure CORS headers appropriately

### Testing

- [ ] Run full test suite
- [ ] Test authentication flow
- [ ] Upload and query documents
- [ ] Test rate limiting
- [ ] Verify error handling
- [ ] Load test with production scale
- [ ] Test file upload with large PDFs

---

## 🚀 Deployment Options

### Option 1: Docker (Recommended)

#### Create Dockerfile for Backend

```dockerfile
# Dockerfile.backend
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY apps/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY apps/backend/app ./app
COPY apps/backend/data ./data

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Create Dockerfile for Frontend

```dockerfile
# Dockerfile.frontend
FROM node:18-alpine as build

WORKDIR /app
COPY apps/frontend/package*.json ./
RUN npm ci

COPY apps/frontend/ .
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app
RUN npm install -g http-server

COPY --from=build /app/dist ./dist

EXPOSE 4200
CMD ["http-server", "dist/apps/frontend", "-p", "4200", "-s"]
```

#### Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - JWT_ALGORITHM=HS256
      - JWT_EXPIRE_MINUTES=60
    volumes:
      - ./apps/backend/data:/app/data
      - ./apps/backend/chroma_db:/app/chroma_db
      - ./apps/backend/uploads:/app/uploads
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "80:4200"
    environment:
      - API_URL=http://localhost:8000
    depends_on:
      - backend
    restart: unless-stopped
```

#### Deploy with Docker

```bash
# Build images
docker-compose build

# Run containers
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down

# Update to new version
git pull
docker-compose build --no-cache
docker-compose up -d
```

---

### Option 2: Traditional Deployment (Nginx + Gunicorn)

#### Backend Setup

```bash
# Install production dependencies
pip install gunicorn==21.2.0

# Create systemd service
sudo nano /etc/systemd/system/aka-backend.service
```

```ini
[Unit]
Description=AI Knowledge Assistant Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/aka-backend
Environment="PATH=/var/www/aka-backend/venv/bin"
ExecStart=/var/www/aka-backend/venv/bin/gunicorn \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile /var/log/aka/backend.access.log \
  --error-logfile /var/log/aka/backend.error.log \
  app.main:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable aka-backend
sudo systemctl start aka-backend
```

#### Frontend Setup

```bash
# Build for production
npm run build

# Copy to web server
sudo cp -r dist/apps/frontend /var/www/aka-frontend
sudo chown -R www-data /var/www/aka-frontend
```

#### Nginx Configuration

```nginx
# /etc/nginx/sites-available/aka

server {
    listen 80;
    server_name api.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;

    # Proxy to backend
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    root /var/www/aka-frontend;
    index index.html;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Content-Type-Options "nosniff" always;

    # SPA routing
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/aka /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

### Option 3: Cloud Platforms

#### Vercel (Frontend Only)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd apps/frontend
vercel --prod

# Configure environment
# Vercel Dashboard → Project Settings → Environment Variables
# Add: NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

#### Heroku (Full Stack)

```bash
# Create Procfile
cat > Procfile << 'EOF'
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT app.main:app
EOF

# Deploy
heroku create aka-production
heroku config:set GOOGLE_API_KEY=...
heroku config:set JWT_SECRET_KEY=...
git push heroku main
```

#### Railway.app

- Connect GitHub repository
- Auto-deploys on push to main
- Set environment variables in dashboard
- Database available via PostgreSQL addon

#### AWS EC2

```bash
# Launch instance (Ubuntu 22.04)
# Security Group: Allow 80, 443, 22

# SSH into instance
ssh -i key.pem ubuntu@instance-ip

# Install dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip nodejs npm nginx certbot python3-certbot-nginx -y

# Clone repository
git clone https://github.com/your-repo.git
cd ai-knowledge-assistant

# Setup backend
cd apps/backend
pip3 install -r requirements.txt
# ... (setup as above)

# Setup frontend
cd ../frontend
npm install
npm run build

# Deploy (use Nginx + Gunicorn as above)
```

---

## 📦 Environment Variables

### Backend (.env)

```env
# Required
GOOGLE_API_KEY=your-api-key-here
JWT_SECRET_KEY=your-long-secret-key-min-32-chars

# Optional (with defaults)
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
API_HOST=0.0.0.0
API_PORT=8000

# Optional: Database (if migrating from JSON)
DATABASE_URL=postgresql://user:password@localhost/aka_db
```

### Frontend (environment.prod.ts)

```typescript
export const environment = {
  production: true,
  apiBaseUrl: 'https://api.yourdomain.com'
};
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install backend deps
        run: pip install -r apps/backend/requirements.txt

      - name: Run backend tests
        run: cd apps/backend && pytest tests/

      - name: Set up Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install frontend deps
        run: cd apps/frontend && npm install

      - name: Run frontend tests
        run: cd apps/frontend && npm test -- --watch=false

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: success()

    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Docker Registry
        run: |
          echo ${{ secrets.DOCKER_PASS }} | docker login -u ${{ secrets.DOCKER_USER }} --password-stdin
          docker build -f Dockerfile.backend -t aka-backend:latest .
          docker push aka-backend:latest

      - name: SSH Deploy
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /var/www/aka
            git pull origin main
            docker pull aka-backend:latest
            docker-compose down
            docker-compose up -d
```

---

## 📊 Monitoring & Logging

### Backend Logging

```python
# In app/main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/aka/backend.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Performance Monitoring

```bash
# Monitor processes
top
ps aux | grep gunicorn
ps aux | grep node

# Check disk space
df -h

# Check vector database size
du -sh chroma_db/

# Check logs
tail -f /var/log/aka/backend.log
tail -f /var/log/nginx/error.log
```

### Uptime Monitoring

- Use UptimeRobot for health checks
- Point to: `https://yourdomain.com/` (health endpoint)
- Alert on failure

---

## 🔄 Updating to New Version

```bash
# Pull latest changes
git pull origin main

# Backup data
cp -r chroma_db chroma_db.backup
cp -r uploads uploads.backup
cp data/users.json data/users.json.backup

# Backend
cd apps/backend
pip install -r requirements.txt
# (restart service)

# Frontend
cd apps/frontend
npm install
npm run build
# (copy to web server)

# If using Docker
docker-compose build --no-cache
docker-compose down
docker-compose up -d
```

---

## 🚨 Troubleshooting Deployment

### Service Won't Start

```bash
# Check logs
systemctl status aka-backend
journalctl -u aka-backend -n 50

# Common issues
# 1. Port already in use
sudo lsof -i :8000 | grep LISTEN
# 2. Permission denied
sudo chown -R www-data /var/www/aka-backend
# 3. Missing environment variables
cat .env  # Check all required vars are set
```

### High Memory Usage

```bash
# Check what's using memory
ps aux --sort=-%mem | head -20

# Reduce worker count
# In Gunicorn: --workers 2
# In browser: limit file upload size
```

### Slow API Responses

```bash
# Check network
ping api.yourdomain.com

# Check database
# Monitor ChromaDB performance
# Consider PostgreSQL if scaling

# Check logs for errors
tail -f /var/log/aka/backend.log
```

---

## 📝 Rollback Procedure

If deployment goes wrong:

```bash
# Stop services
docker-compose down
# or
sudo systemctl stop aka-backend

# Restore from backup
rm -rf chroma_db
cp -r chroma_db.backup chroma_db

# Revert code
git revert HEAD
git push origin main

# Restart
docker-compose up -d
# or
sudo systemctl start aka-backend
```

---

## 🔒 Security Best Practices

1. **Keep secrets out of git**
   - Use `.env` (in `.gitignore`)
   - Use environment variables in CI/CD
   - Rotate keys regularly

2. **HTTPS only**
   - Use Let's Encrypt for SSL
   - Enforce HTTPS redirects
   - Set HSTS headers

3. **Update dependencies**
   ```bash
   # Security updates
   pip install --upgrade pip
   pip list --outdated
   npm audit
   npm update
   ```

4. **Regular backups**
   ```bash
   # Daily backup script
   #!/bin/bash
   DATE=$(date +%Y%m%d)
   tar -czf /backups/aka-$DATE.tar.gz \
     /var/www/aka-backend/chroma_db \
     /var/www/aka-backend/data \
     /var/www/aka-backend/uploads
   ```

5. **Monitor access logs**
   ```bash
   grep "4[0-9][0-9]" /var/log/nginx/access.log | wc -l  # 4xx errors
   grep "5[0-9][0-9]" /var/log/nginx/access.log | wc -l  # 5xx errors
   ```

---

## 📚 Deployment Checklist

- [ ] Pre-deployment security review
- [ ] Test all features on staging
- [ ] Generate new JWT secret key
- [ ] Update API URLs in frontend config
- [ ] Update CORS settings
- [ ] Setup monitoring & logging
- [ ] Setup backups
- [ ] Deploy database (if needed)
- [ ] Deploy backend
- [ ] Deploy frontend
- [ ] Test in production
- [ ] Monitor for issues
- [ ] Document deployment steps

---

**Last Updated**: March 29, 2026
**Status**: Production Ready ✅
