# LAN Access & Server Deployment Guide

## 🌐 Accessing via LAN (Local Network)

### Option 1: Development Server (Easiest)

#### Step 1: Find Your Machine's IP Address

**macOS/Linux:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
# Look for 192.168.x.x or 10.0.x.x
```

**Windows (Command Prompt):**
```cmd
ipconfig
# Look for "IPv4 Address" under your network adapter
```

#### Step 2: Update Django Settings

Edit `joyland/settings.py` and modify ALLOWED_HOSTS:

```python
# For development with LAN access:
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.x.x', '*']
# Replace 192.168.x.x with YOUR actual IP from Step 1
```

Or use environment variable (better practice):

Create `.env` file:
```
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,192.168.x.x
```

#### Step 3: Run Server with Network Access

```bash
# Bind to all network interfaces
python manage.py runserver 0.0.0.0:8000

# Or specify your IP
python manage.py runserver 192.168.x.x:8000
```

#### Step 4: Access from LAN Devices

On any device on your network:
```
http://192.168.x.x:8000/
```

**Example:**
- Main machine: `192.168.1.100`
- From laptop on same network: `http://192.168.1.100:8000/`
- Admin panel: `http://192.168.1.100:8000/admin/`

---

## 🖥️ Server Deployment (Production)

### Prerequisites
- Server/VPS with Ubuntu/Debian or similar Linux
- Python 3.9+ installed
- SSH access to server
- Domain name (optional but recommended)

### Option A: Simple Deployment with Gunicorn + Nginx

#### Step 1: Connect to Server

```bash
ssh user@your-server-ip
# Or use your hosting provider's console
```

#### Step 2: Install System Dependencies

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx git postgresql postgresql-contrib
```

#### Step 3: Clone Project

```bash
cd /home/username
git clone https://github.com/officialfelixmunyany-ctrl/joylandschools.git
cd joylandschools/backend
```

#### Step 4: Setup Python Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

#### Step 5: Configure Database (PostgreSQL)

```bash
# Connect to PostgreSQL
sudo -u postgres psql

# In psql console, run:
CREATE DATABASE joyland_db;
CREATE USER joyland_user WITH PASSWORD 'strong-password-here';
ALTER ROLE joyland_user SET client_encoding TO 'utf8';
ALTER ROLE joyland_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE joyland_user SET default_transaction_deferrable TO on;
ALTER ROLE joyland_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE joyland_db TO joyland_user;
\q
```

#### Step 6: Update Django Settings

Edit `joyland/settings.py`:

```python
# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'joyland_db',
        'USER': 'joyland_user',
        'PASSWORD': 'strong-password-here',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Security settings for production
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com', 'your-server-ip']
SECRET_KEY = 'your-secure-secret-key-here'
```

Or use environment variables (recommended):

Create `.env` file on server:
```bash
DEBUG=False
DJANGO_SECRET_KEY=your-secure-secret-key-here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://joyland_user:strong-password@localhost/joyland_db
OPENAI_API_KEY=your-openai-key-if-using
```

Update settings.py to use:
```python
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
```

#### Step 7: Run Migrations

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

#### Step 8: Create Gunicorn Service

Create `/etc/systemd/system/gunicorn_joyland.service`:

```ini
[Unit]
Description=Joyland Schools Gunicorn Application Server
After=network.target

[Service]
Type=notify
User=username
Group=www-data
WorkingDirectory=/home/username/joylandschools/backend
Environment="PATH=/home/username/joylandschools/backend/venv/bin"
ExecStart=/home/username/joylandschools/backend/venv/bin/gunicorn \
          --workers 3 \
          --worker-class sync \
          --bind unix:/tmp/gunicorn_joyland.sock \
          --timeout 30 \
          --access-logfile - \
          --error-logfile - \
          joyland.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable gunicorn_joyland
sudo systemctl start gunicorn_joyland
sudo systemctl status gunicorn_joyland
```

#### Step 9: Configure Nginx

Create `/etc/nginx/sites-available/joyland`:

```nginx
upstream gunicorn_joyland {
    server unix:/tmp/gunicorn_joyland.sock fail_timeout=0;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    client_max_body_size 10M;

    location /static/ {
        alias /home/username/joylandschools/backend/static/;
    }

    location /media/ {
        alias /home/username/joylandschools/backend/media/;
    }

    location / {
        proxy_pass http://gunicorn_joyland;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/joyland /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 10: Setup SSL (HTTPS) with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

#### Step 11: Setup Logs and Monitoring

```bash
# Create log directory
sudo mkdir -p /var/log/joyland
sudo chown username:www-data /var/log/joyland

# View logs
sudo journalctl -u gunicorn_joyland -f
sudo tail -f /var/log/nginx/access.log
```

---

### Option B: Docker Deployment (Recommended for Scalability)

#### Step 1: Create Dockerfile

Create `Dockerfile` in backend directory:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "joyland.wsgi:application"]
```

#### Step 2: Create docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: joyland_db
      POSTGRES_USER: joyland_user
      POSTGRES_PASSWORD: strong-password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: ./backend
    command: >
      sh -c "python manage.py migrate &&
             python manage.py createsuperuser --noinput ||
             true &&
             gunicorn --bind 0.0.0.0:8000 joyland.wsgi:application"
    environment:
      DEBUG: "False"
      DJANGO_SECRET_KEY: "your-secret-key"
      ALLOWED_HOSTS: "your-domain.com,localhost"
      DATABASE_URL: "postgresql://joyland_user:strong-password@db:5432/joyland_db"
    volumes:
      - ./backend:/app
      - static_volume:/app/staticfiles
    ports:
      - "8000:8000"
    depends_on:
      - db

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - static_volume:/app/staticfiles:ro
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
```

#### Step 3: Run Docker

```bash
docker-compose up -d
docker-compose logs -f
```

---

## 🔒 Security Checklist for Production

- [ ] Set `DEBUG = False` in settings
- [ ] Use strong `SECRET_KEY` (generate new one)
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Use HTTPS/SSL certificate
- [ ] Set `SECURE_SSL_REDIRECT = True` in settings
- [ ] Configure `CSRF_TRUSTED_ORIGINS`
- [ ] Use environment variables for secrets
- [ ] Setup database backups
- [ ] Monitor logs and errors
- [ ] Setup fail2ban for brute force protection
- [ ] Keep dependencies updated (`pip list --outdated`)

### Add to production settings.py:

```python
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

---

## 📊 Monitoring & Maintenance

### Check Server Status
```bash
# Gunicorn
sudo systemctl status gunicorn_joyland

# Nginx
sudo systemctl status nginx

# Database
sudo systemctl status postgresql

# System resources
top
df -h
free -h
```

### View Logs
```bash
# Django errors
sudo journalctl -u gunicorn_joyland -n 50

# Nginx access
sudo tail -f /var/log/nginx/access.log

# Nginx errors
sudo tail -f /var/log/nginx/error.log

# Django app logs
tail -f backend/logs/joyland.log
```

### Backup Database
```bash
# Manual backup
sudo -u postgres pg_dump joyland_db > joyland_backup.sql

# Restore from backup
sudo -u postgres psql joyland_db < joyland_backup.sql

# Automated backup (add to crontab)
0 2 * * * sudo -u postgres pg_dump joyland_db > /backups/joyland_$(date +\%Y\%m\%d).sql
```

---

## 🚀 Quick Comparison

| Method | Ease | Performance | Scalability | Cost |
|--------|------|-------------|-------------|------|
| Dev Server (LAN) | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | Free |
| Gunicorn + Nginx | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Low |
| Docker Compose | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Low |
| Kubernetes | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Medium |

---

## 📱 Testing on Mobile Devices

### Same WiFi Network
```bash
# Find your machine IP
ipconfig getifaddr en0  # macOS
# or
hostname -I  # Linux

# Then visit on phone/tablet:
http://192.168.x.x:8000
```

### Over Internet (Ngrok Tunneling)
```bash
# Install ngrok: https://ngrok.com/
ngrok http 8000

# Share the provided URL with others
# Example: https://abc123.ngrok.io
```

---

## 🆘 Troubleshooting

### Can't access from LAN devices
```bash
# 1. Check if server is running
python manage.py runserver 0.0.0.0:8000

# 2. Check firewall
sudo ufw allow 8000

# 3. Verify IP and port
netstat -tuln | grep 8000

# 4. Check ALLOWED_HOSTS in settings
```

### Gunicorn not starting
```bash
# Check logs
sudo journalctl -u gunicorn_joyland -n 50 --no-pager

# Restart
sudo systemctl restart gunicorn_joyland
```

### Database connection error
```bash
# Test PostgreSQL
psql -U joyland_user -d joyland_db -h localhost

# Check migrations
python manage.py showmigrations

# Run migrations
python manage.py migrate
```

---

**Choose the option that best fits your needs!** 🎯
