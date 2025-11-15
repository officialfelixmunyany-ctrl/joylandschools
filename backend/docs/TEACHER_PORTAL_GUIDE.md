# Teacher Portal Setup & Deployment Guide

## Overview
This guide explains how to run and view the Joyland Schools teacher portal with AI-powered educational tools.

---

## Prerequisites

### System Requirements
- **Windows 10/11 or macOS/Linux**
- **Python 3.9+** (available in PATH)
- **pip** package manager
- **Git** (optional, but recommended)
- **A code editor** (VS Code, PyCharm, etc.)

### Accounts Required
- **OpenAI API Key** (for GPT models): Get from https://platform.openai.com/api-keys
- **Django superuser** for admin access

---

## Part 1: Initial Setup (One-Time)

### Step 1: Navigate to Project Root
Open PowerShell and navigate to the project root:

```powershell
cd C:\Users\STUDENT\Desktop\DATA\projects\joylandschools
```

### Step 2: Create a Virtual Environment (Recommended)
Create an isolated Python environment:

```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# If you get an execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then activate again
```

### Step 3: Install Dependencies
Install required packages:

```powershell
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Key packages installed:
- `Django` - Web framework
- `djangorestframework` - REST API support
- `openai` - GPT integration
- `django-redis` - Caching backend
- `python-dotenv` - Environment variable management

### Step 4: Environment Configuration
Create a `.env` file in the `backend` directory:

```bash
# backend/.env
OPENAI_API_KEY=your_api_key_here
DEBUG=True
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=localhost,127.0.0.1

# Cache Configuration
CACHE_BACKEND=django.core.cache.backends.locmem.LocMemCache
CACHE_AI_RESULTS=True
```

If using Redis/Memcached for production (optional):

```bash
# For Redis
CACHE_BACKEND=django_redis.cache.RedisCache
CACHE_URL=redis://127.0.0.1:6379/1

# For Memcached
CACHE_BACKEND=django.core.cache.backends.memcached.MemcachedCache
CACHE_LOCATION=127.0.0.1:11211
```

### Step 5: Database Setup
Initialize the database:

```powershell
# Apply migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
# Follow prompts:
# - Username: admin
# - Email: admin@joyland.edu
# - Password: (create secure password)

# Create a test teacher account
python manage.py shell
```

In the Django shell:
```python
from users.models import User

# Create a teacher
teacher = User.objects.create_user(
    username='teacher1',
    email='teacher1@joyland.edu',
    password='testpass123',
    role='teacher',
    first_name='John',
    last_name='Doe'
)
print(f"Teacher created: {teacher.username}")
exit()
```

---

## Part 2: Running the Portal

### Step 1: Start the Development Server

```powershell
# Make sure you're in backend/ and .venv is activated
cd C:\Users\STUDENT\Desktop\DATA\projects\joylandschools\backend

# If not activated:
.\.venv\Scripts\Activate.ps1

# Start Django development server
python manage.py runserver
```

Expected output:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
November 11, 2025 - HH:MM:SS
Django version 4.x, using settings 'joyland.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Step 2: Access the Portal

Open your web browser and navigate to:

#### Teacher Login
```
http://127.0.0.1:8000/users/portal/login/
```

**Login Credentials:**
- Username: `teacher1`
- Password: `testpass123`

#### Admin Panel
```
http://127.0.0.1:8000/admin/
```

**Login with superuser credentials** (from Step 5 above)

---

## Part 3: Using the Teacher Portal

### Dashboard Access
After logging in as a teacher, you'll see the dashboard at:
```
http://127.0.0.1:8000/users/portal/teacher/
```

### AI-Powered Features

#### 1. Term Planning
Generate learning objectives for an entire term:

1. Navigate to **"Term Planning"** section
2. Select **Subject** (e.g., Mathematics)
3. Select **Grade Level** (e.g., 9th)
4. Choose **Term** (1, 2, or 3)
5. Click **"Generate Term Plan"**
6. AI generates learning objectives with skills and assessment criteria
7. Results are cached for 24 hours for faster subsequent access

**What it does:**
- Creates curriculum aligned with educational standards
- Suggests learning objectives by topic
- Provides assessment criteria
- Prevents duplication of previously covered topics

#### 2. Assessment Generator
Create differentiated assessments for any learning objective:

1. Navigate to **"Assessment Generator"** section
2. Enter a **Learning Objective** (e.g., "Solve quadratic equations")
3. Select **Assessment Type** (Formative/Summative/Diagnostic)
4. Choose **Student Level** (Support/Standard/Extension)
5. Click **"Generate Assessment"**
6. AI creates multiple assessment items with:
   - Questions tailored to student level
   - Rubrics for grading
   - Sample answers
   - Point values

#### 3. Class Overview
View your class composition:

1. See **"Class Overview"** table
2. View student distribution by level:
   - **Support Level** - Students needing extra help
   - **Standard Level** - Grade-level learners
   - **Extension Level** - Advanced students
3. Click **"Generate Activities"** to create differentiated lessons

#### 4. Differentiated Activities
Generate activities for different student levels in one class:

1. Click **"Generate Activities"** on any class
2. Enter the **Learning Objective**
3. AI generates three sets of activities:
   - **Support Level Activities** - Scaffolded, guided practice
   - **Standard Level Activities** - Grade-level learning
   - **Extension Level Activities** - Challenging, higher-order thinking
4. Each activity includes:
   - Description and learning approach
   - Required materials
   - Estimated duration

---

## Part 4: Performance & Caching

### How Caching Works

All AI-generated content is automatically cached:

- **Cache Duration:** 24 hours (configurable)
- **Cache Key:** Includes teacher ID + parameters (subject, grade, term, etc.)
- **Cache Backend:** Defaults to local memory; can use Redis for production

**Indicators:**
- When content is cached, a "⚡ From Cache" badge appears
- Cached results load instantly (typically < 100ms)
- First generation takes longer (depends on OpenAI API response time)

### Clearing Cache (if needed)

In Django shell:
```python
from django.core.cache import cache
cache.clear()  # Clear all cache
```

Or in Python code:
```python
from joyland.cache_utils import AIOperationCache
AIOperationCache.clear_teacher_cache(teacher_id=1)
```

---

## Part 5: Testing

### Run Unit Tests

```powershell
# Run all teacher view tests
python manage.py test users.tests.test_teacher_views -v 2

# Run specific test
python manage.py test users.tests.test_teacher_views.TeacherViewsTest.test_teacher_dashboard_access

# Run with coverage
coverage run --source='.' manage.py test users.tests.test_teacher_views
coverage report
coverage html  # Creates htmlcov/index.html
```

### Expected Test Results
All tests should pass:
- ✅ Access permissions (only teachers can access)
- ✅ Term plan generation
- ✅ Assessment creation
- ✅ Student progress analysis
- ✅ Activity generation
- ✅ Error handling and validation

---

## Part 6: Troubleshooting

### Issue: "Python not found"
**Solution:** Install Python from https://www.python.org/downloads/
Ensure "Add Python to PATH" is checked during installation.

### Issue: "ModuleNotFoundError: No module named 'X'"
**Solution:** Ensure virtual environment is activated and dependencies are installed:
```powershell
pip install -r requirements.txt
```

### Issue: "No installed Python found"
**Solution:** Use full path or ensure Python is in PATH:
```powershell
# Check if python works
python --version

# If not, use full path to Python executable
C:\Python311\python.exe manage.py runserver
```

### Issue: "OpenAI API Error"
**Solution:** Verify your API key:
1. Check `.env` file has correct `OPENAI_API_KEY`
2. Verify key at https://platform.openai.com/api-keys
3. Ensure you have API credits available
4. Check rate limits: https://platform.openai.com/account/rate-limits

### Issue: "CSRF token missing"
**Solution:** Ensure you're:
1. Logged in as a teacher
2. Using Django development server (not accessing from different domain)
3. Cookies are enabled in browser

### Issue: "Database connection error"
**Solution:** Ensure SQLite database exists:
```powershell
python manage.py migrate
```

---

## Part 7: Production Deployment (Optional)

### For Deploying to a Server

1. **Set DEBUG = False** in settings
2. **Use a production cache backend** (Redis/Memcached)
3. **Configure ALLOWED_HOSTS**
4. **Use a production WSGI server** (Gunicorn, uWSGI)
5. **Set up SSL/TLS** (HTTPS)
6. **Configure static files** collection with `collectstatic`
7. **Set up logging and monitoring**

Example with Gunicorn:
```powershell
pip install gunicorn
gunicorn joyland.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

---

## Part 8: Architecture Overview

```
┌─────────────────────────────────────┐
│   Teacher Dashboard (Frontend)      │
│   - HTML/Bootstrap UI               │
│   - JavaScript (Fetch API)          │
└────────────────┬────────────────────┘
                 │ HTTP/JSON
┌────────────────▼────────────────────┐
│   Django Backend                    │
│   - users/views/teacher.py          │
│   - REST API endpoints              │
└────────────────┬────────────────────┘
                 │
    ┌────────────┴────────────┬──────────────┐
    │                         │              │
┌───▼────────────┐ ┌─────────▼────┐ ┌──────▼──────┐
│  Cache Layer   │ │ Database     │ │ OpenAI API  │
│ (Redis/Memory) │ │ (SQLite/Pg)  │ │ (GPT-4 mini)│
└────────────────┘ └──────────────┘ └─────────────┘
```

### Key Files

```
backend/
├── users/
│   ├── views/
│   │   ├── teacher.py          # ✨ Teacher dashboard views
│   │   ├── auth.py             # Login/logout
│   │   ├── registration.py     # User registration
│   │   └── announcements.py    # Announcements management
│   ├── models.py               # User model with role field
│   ├── urls.py                 # URL routing
│   └── tests/
│       └── test_teacher_views.py  # ✅ Teacher view tests
├── joyland/
│   ├── integrations/
│   │   ├── openai.py          # OpenAI API client
│   │   └── education.py       # ✨ Educational AI services
│   ├── cache_utils.py         # ✨ Caching utilities
│   ├── settings.py            # Django configuration
│   └── urls.py                # Main URL config
├── templates/
│   └── users/
│       └── teacher_dashboard.html  # ✨ Teacher dashboard template
├── manage.py                   # Django CLI
└── requirements.txt            # Python dependencies
```

---

## Summary Commands

**Quick Start (after initial setup):**
```powershell
# 1. Navigate to backend
cd C:\Users\STUDENT\Desktop\DATA\projects\joylandschools\backend

# 2. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 3. Start server
python manage.py runserver

# 4. Open browser
# Teacher login: http://127.0.0.1:8000/users/portal/login/
# (user: teacher1, pass: testpass123)

# 5. Access dashboard
# http://127.0.0.1:8000/users/portal/teacher/
```

**Stop Server:** Press `Ctrl+C` in PowerShell

---

## Next Steps

After getting the portal running:

1. ✅ **Customize teacher data** - Update `get_teacher_subjects()` to pull from database
2. ✅ **Add real student data** - Connect `get_student_data()` to actual student records
3. ✅ **Configure email** - Set up Django email for notifications
4. ✅ **Add export features** - Export plans/assessments as PDF/Word
5. ✅ **Set up user authentication** - Integrate with school's LDAP/Active Directory

---

## Support & Documentation

- **Django Docs:** https://docs.djangoproject.com/
- **OpenAI API:** https://platform.openai.com/docs/
- **Bootstrap:** https://getbootstrap.com/docs/
- **Project README:** See `backend/README_DEV.md`

---

**Last Updated:** November 11, 2025  
**Version:** 1.0.0  
**Author:** AI Assistant
