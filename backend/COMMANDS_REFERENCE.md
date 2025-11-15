# Quick Reference - Commands & Setup

## 🚀 Start Development (5 seconds)

```bash
cd joylandschools/backend
source venv/bin/activate          # or: venv\Scripts\activate (Windows)
python manage.py runserver
# Visit: http://127.0.0.1:8000/
```

## 🌐 Access from LAN Devices

### Find Your IP
```bash
# macOS/Linux
ifconfig | grep "inet " | grep -v 127.0.0.1

# Windows
ipconfig
```

### Start Server for LAN
```bash
python manage.py runserver 0.0.0.0:8000
# Or: python manage.py runserver 192.168.x.x:8000
```

### Access from Other Devices
```
http://192.168.x.x:8000/
http://192.168.x.x:8000/admin/
```

## 🖥️ Deployment Approaches

### 1. Simple Server (Gunicorn + Nginx)
```bash
# Install
pip install gunicorn
sudo apt install nginx postgresql

# Run
gunicorn --bind 0.0.0.0:8000 joyland.wsgi:application
```

### 2. Docker (Recommended)
```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f
```

### 3. Auto-start on Server Reboot
```bash
# Create systemd service
sudo systemctl enable gunicorn_joyland
sudo systemctl start gunicorn_joyland
sudo systemctl status gunicorn_joyland
```

## 🔧 Common Django Commands

```bash
# Database
python manage.py migrate              # Apply migrations
python manage.py makemigrations       # Create migrations
python manage.py showmigrations       # View migration status

# Admin
python manage.py createsuperuser      # Create admin account
python manage.py changepassword       # Change user password

# Static files
python manage.py collectstatic        # Collect for production

# Utilities
python manage.py shell                # Interactive Python shell
python manage.py test                 # Run tests
python manage.py check                # Check configuration

# Create new app
python manage.py startapp myapp
```

## 📝 Environment Setup (.env file)

Create in `backend/.env`:
```
# Django
DEBUG=True
DJANGO_SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,192.168.x.x

# Database (if using PostgreSQL)
DATABASE_URL=postgresql://user:pass@localhost/dbname

# OpenAI (optional)
OPENAI_API_KEY=sk-your-key

# Logging
DJANGO_LOG_LEVEL=INFO
```

## 🔐 Ports & Access

| Service | Port | URL |
|---------|------|-----|
| Dev Server | 8000 | http://127.0.0.1:8000 |
| Admin | 8000 | http://127.0.0.1:8000/admin |
| Nginx (Prod) | 80 | http://your-domain.com |
| PostgreSQL | 5432 | localhost:5432 |

## 🐛 Troubleshooting

```bash
# Port already in use
lsof -i :8000                         # Check what's using port 8000
kill -9 <PID>                         # Kill the process
python manage.py runserver 8001       # Use different port

# Module not found
pip install -r requirements.txt

# Migration issues
python manage.py migrate --fake-initial
python manage.py migrate --plan

# Database errors
python manage.py dbshell              # Access database CLI

# Static files not loading
python manage.py collectstatic
python manage.py findstatic <filename>

# Check system health
python manage.py check
```

## 📊 Server Status

```bash
# Check if running
curl http://127.0.0.1:8000/

# View logs (production)
sudo journalctl -u gunicorn_joyland -f

# Monitor system
top
df -h
free -h

# Check database
psql -U joyland_user -d joyland_db
```

## 🔄 Restart After Changes

```bash
# For development (auto-reloads usually)
# Just save the file

# For production
sudo systemctl restart gunicorn_joyland
sudo systemctl restart nginx

# Or with Docker
docker-compose restart web
docker-compose restart nginx
```

## 📚 Full Documentation

- **README.md** — Main documentation
- **QUICKSTART.md** — 5-minute setup
- **docs/LAN_AND_DEPLOYMENT.md** — This detailed guide
- **docs/README_DEV.md** — Development guidelines
- **docs/README_SETUP.md** — Detailed installation

## 🚨 Critical Settings for Production

```python
# In joyland/settings.py or .env:
DEBUG = False                          # MUST be False
SECRET_KEY = 'unique-long-secret'      # MUST be unique and secret
ALLOWED_HOSTS = ['your-domain.com']    # Add your domain
SECURE_SSL_REDIRECT = True             # Force HTTPS
SESSION_COOKIE_SECURE = True           # HTTPS only cookies
CSRF_COOKIE_SECURE = True              # HTTPS only CSRF
```

## 💡 Pro Tips

1. **Use environment variables** - Never commit secrets to git
2. **Always use HTTPS** - For any public deployment
3. **Backup your database** - Regularly and before updates
4. **Monitor logs** - Check logs regularly for errors
5. **Keep dependencies updated** - Run `pip install --upgrade -r requirements.txt`
6. **Use a process manager** - systemd, supervisor, or docker
7. **Setup SSL certificate** - Use Let's Encrypt (free)
8. **Test locally first** - Deploy to prod only after testing

## 🎯 Typical Workflow

```bash
# 1. Start work
source venv/bin/activate
python manage.py runserver

# 2. Make changes
# (edit files in your IDE)

# 3. Create database changes if needed
python manage.py makemigrations
python manage.py migrate

# 4. Test
python manage.py test
curl http://localhost:8000/

# 5. Commit and push
git add .
git commit -m "Your message"
git push origin main

# 6. Deploy to server
# (follow deployment section above)
```

---

**Need more help?** Check the full documentation in `/docs/`
