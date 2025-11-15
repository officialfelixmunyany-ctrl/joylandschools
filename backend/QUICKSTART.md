# Quick Start Guide - Joyland Schools Backend

Get the Django backend running in 5 minutes!

## Prerequisites
- Python 3.9+ installed
- Terminal/Command Prompt access
- Git (for cloning)

## Installation Steps

### 1. Clone Repository
```bash
cd Desktop
git clone https://github.com/officialfelixmunyany-ctrl/joylandschools.git
cd joylandschools/backend
```

### 2. Create Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows (Command Prompt)
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Create Admin User
```bash
python manage.py createsuperuser
# Follow prompts to create your account
```

### 6. Start Development Server
```bash
python manage.py runserver
```

## Access the Application

- **Landing Page:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/
- **Teacher Login:** http://127.0.0.1:8000/users/portal/login/

## Common Commands

```bash
# Create new app
python manage.py startapp <app_name>

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run tests
python manage.py test

# Open Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic

# Create superuser
python manage.py createsuperuser

# Run with custom port
python manage.py runserver 8001
```

## Troubleshooting

### Virtual Environment Issues
```bash
# Deactivate current environment
deactivate

# Reactivate
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Port 8000 Already in Use
```bash
python manage.py runserver 8001
```

### Reset Database
```bash
# Delete existing database
rm db.sqlite3

# Run migrations fresh
python manage.py migrate

# Create new superuser
python manage.py createsuperuser
```

## Project Structure

```
backend/
├── manage.py              ← Django management command
├── README.md              ← Full documentation
├── requirements.txt       ← Python dependencies
│
├── joyland/               ← Main Django project
│   └── settings.py        ← Configuration
│
├── core/                  ← Content app (announcements, events)
├── users/                 ← User authentication
│
├── templates/             ← HTML files
├── static/                ← CSS, JS, images
└── docs/                  ← Documentation
```

## Development Tips

### Use environment variables
Create `.env` file:
```
DEBUG=True
DJANGO_SECRET_KEY=your-secret-key
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

### Enable Debug Toolbar (optional)
```bash
pip install django-debug-toolbar
```

### Run with auto-reload
```bash
python manage.py runserver --reload
```

### Check database migrations
```bash
python manage.py showmigrations
```

## Next Steps

1. **Read the full README:** See `README.md` for comprehensive docs
2. **Explore the admin:** Login to http://127.0.0.1:8000/admin/
3. **Check out the docs:** Review `docs/README_DEV.md` for development guidelines
4. **Start building:** Begin modifying views, templates, and models

## Need Help?

1. **Check the docs:** `docs/` folder has detailed guides
2. **Django docs:** https://docs.djangoproject.com/
3. **Project issues:** Check GitHub issues for known problems

---

Happy coding! 🚀
