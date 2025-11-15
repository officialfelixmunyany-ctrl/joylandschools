# JoylandSchools Backend (Django)

This is a starter Django backend for Joyland Schools with a custom `User` model and a `users` app.

Quick start (Windows PowerShell):

1. Create and activate a virtualenv

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install requirements

```powershell
pip install -r requirements.txt
```

3. Run migrations and create superuser

```powershell
python manage.py migrate; python manage.py createsuperuser
```

4. Run the development server

```powershell
python manage.py runserver
```

The admin UI is available at http://127.0.0.1:8000/admin/ and the landing page at http://127.0.0.1:8000/.

Fixing roles
-----------
If you find that superusers or admins were accidentally created with role 'student', run:

```powershell
python manage.py fix_roles --fix-superusers
```

This will update all superusers in the database so their role is `system_admin`.
