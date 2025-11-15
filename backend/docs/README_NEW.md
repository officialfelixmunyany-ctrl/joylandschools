# JoylandSchools Backend (Django)

Fully functional Django backend for Joyland Schools with AI-powered teacher portal.

## 🚀 Quick Start

### First Time Setup
**IMPORTANT:** Python 3.11+ must be installed and in PATH

See detailed guide: **[README_SETUP.md](README_SETUP.md)** (15-minute setup)

### Quick Commands (After Python installed)
```cmd
REM Use Command Prompt (cmd), NOT PowerShell
cd C:\Users\STUDENT\Desktop\DATA\projects\joylandschools\backend
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then open: http://127.0.0.1:8000/users/portal/login/
- Username: `teacher1`
- Password: `testpass123`

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **[README_SETUP.md](README_SETUP.md)** | Complete setup overview & checklist |
| **[QUICK_START_MANUAL.md](QUICK_START_MANUAL.md)** | Step-by-step manual setup guide |
| **[TEACHER_PORTAL_GUIDE.md](TEACHER_PORTAL_GUIDE.md)** | Full portal features & usage |
| **[PYTHON_INSTALLATION_FIX.md](PYTHON_INSTALLATION_FIX.md)** | Python installation help |

## ✨ Features

- 📋 **AI-Powered Term Planning** - Generate curriculum objectives
- 📝 **Assessment Generator** - Create differentiated tests
- 👥 **Class Overview** - View student distribution by level
- 🎯 **Activity Generator** - Level-specific learning activities
- ⚡ **Smart Caching** - Instant results for repeated requests
- 🔄 **Progress Indicators** - Real-time loading feedback
- ✅ **Full Test Coverage** - 8 comprehensive unit tests

## 🏗️ Project Structure

```
backend/
├── users/                      # User management & teacher portal
│   ├── views/
│   │   ├── teacher.py         # ✨ AI-powered teacher dashboard
│   │   ├── auth.py            # Login/logout
│   │   ├── registration.py    # User registration
│   │   └── announcements.py   # Announcements
│   ├── models.py              # User model with roles
│   ├── urls.py                # URL routing
│   └── tests/
│       └── test_teacher_views.py  # ✅ Unit tests
├── joyland/                    # Main project
│   ├── integrations/
│   │   ├── openai.py          # 🤖 OpenAI API integration
│   │   └── education.py       # 🎓 Educational AI services
│   ├── cache_utils.py         # ⚡ Caching utilities
│   ├── settings.py            # Django configuration
│   └── urls.py                # Main URL config
├── templates/users/
│   └── teacher_dashboard.html # 💻 Dashboard UI
├── manage.py                  # Django CLI
└── db.sqlite3                 # Database
```

## 🔧 Configuration

### Environment Variables (.env file)
```
DEBUG=True
SECRET_KEY=django-insecure-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1
OPENAI_API_KEY=your_openai_api_key_here
CACHE_AI_RESULTS=True
```

### Get OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Add to `.env` file

## 🧪 Testing

Run unit tests:
```cmd
python manage.py test users.tests.test_teacher_views -v 2
```

Expected: ✅ All 8 tests PASS

## 📊 Available Endpoints

### Teacher Portal
- `GET /users/portal/teacher/` - Dashboard
- `POST /users/portal/teacher/generate-term-plan/` - Generate curriculum
- `POST /users/portal/teacher/generate-assessment/` - Create tests
- `POST /users/portal/teacher/analyze-student/` - Student progress
- `POST /users/portal/teacher/get-differentiated-activities/` - Level-based activities

### Authentication
- `GET /users/portal/login/` - Login page
- `POST /users/portal/logout/` - Logout
- `GET /users/portal/register/` - Registration selection

### Admin
- `GET /admin/` - Django admin interface

## 🔐 Security Notes

Development setup only. For production:
- Set `DEBUG=False`
- Generate secure `SECRET_KEY`
- Configure `ALLOWED_HOSTS`
- Use HTTPS/SSL
- Set up PostgreSQL
- Configure Redis cache
- Use Gunicorn/uWSGI

## 📞 Troubleshooting

**Python not found?**
→ Install from https://www.python.org/ (check "Add Python to PATH")

**Dependencies won't install?**
→ Run: `pip install --upgrade pip setuptools wheel`

**"Port 8000 already in use"?**
→ Run on different port: `python manage.py runserver 8001`

**Tests failing?**
→ Run migrations first: `python manage.py migrate`

See full troubleshooting in [README_SETUP.md](README_SETUP.md)

## Legacy Commands

Fixing roles (if needed):
```cmd
python manage.py fix_roles --fix-superusers
```

## 📄 License

Copyright © 2025 Joyland Schools. All rights reserved.
