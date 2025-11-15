# Joyland Schools - Django Backend

A modern, modular Django backend for Joyland Schools with user authentication, content management, and AI integrations.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ (Check: `python --version`)
- pip package manager

### Installation (5 minutes)

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Create superuser (admin account)
python manage.py createsuperuser

# 5. Start development server
python manage.py runserver
```

Then visit:
- **Landing**: http://127.0.0.1:8000/
- **Admin**: http://127.0.0.1:8000/admin/
- **Teacher Portal**: http://127.0.0.1:8000/users/portal/login/

### Test Credentials
After creating a superuser, use those credentials to access the admin panel.

## 📁 Project Structure

```
backend/
├── joyland/           # Main Django project settings
├── core/              # Core app (announcements, events, registration)
├── users/             # User authentication & profiles
├── templates/         # HTML templates (organized by app)
├── static/            # CSS, JavaScript, images
├── docs/              # Documentation
└── manage.py          # Django management script
```

## 🔧 Key Features

- **Custom User Model**: Support for multiple roles (Admin, Teacher, Student, Parent)
- **Role-Based Access Control**: Different views and dashboards per role
- **Announcements**: Admin-managed announcements for landing page
- **Registration Requests**: Multi-type registration (Student, Teacher, Parent)
- **Presence Tracking**: Track site visits and engagement
- **AI Integration**: OpenAI integration for student analysis (if configured)

## 🛠 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# Django
DEBUG=True
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# OpenAI (optional)
OPENAI_API_KEY=sk-your-api-key
OPENAI_DEFAULT_MODEL=gpt-4
ENABLE_GPT5_MINI=false
```

### Database

Currently uses SQLite for development. For production, update `DATABASES` in `joyland/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'joyland',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📝 Common Commands

```bash
# Create new app
python manage.py startapp <app_name>

# Create migrations for changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Open Django shell
python manage.py shell

# Create superuser
python manage.py createsuperuser

# Collect static files (production)
python manage.py collectstatic
```

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test users

# Run with verbose output
python manage.py test -v 2
```

## 📚 Additional Documentation

- **[Setup Guide](docs/README_SETUP.md)** - Detailed setup instructions with troubleshooting
- **[Development Guide](docs/README_DEV.md)** - Development workflow and best practices
- **[Teacher Portal Guide](docs/TEACHER_PORTAL_GUIDE.md)** - Teacher-specific features

## 🐛 Troubleshooting

### ModuleNotFoundError: No module named 'X'
```bash
pip install -r requirements.txt
```

### Migration errors
```bash
python manage.py makemigrations
python manage.py migrate
```

### Port 8000 already in use
```bash
python manage.py runserver 8001
```

### Permission denied on Linux/Mac
```bash
chmod +x manage.py
```

## 📋 Project Status

- ✅ User authentication (custom roles)
- ✅ Admin dashboard
- ✅ Announcements system
- ✅ Registration request handling
- ✅ Presence tracking
- ⏳ REST API (planned)
- ⏳ Real-time notifications (planned)

## 👥 Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and test: `python manage.py test`
3. Commit: `git commit -am 'Add feature'`
4. Push: `git push origin feature/your-feature`

## 📄 License

© 2025 Joyland Schools. All rights reserved.

## 🆘 Support

For issues or questions:
1. Check the [troubleshooting section](#troubleshooting)
2. Review documentation in `/docs/`
3. Check Django docs: https://docs.djangoproject.com/
