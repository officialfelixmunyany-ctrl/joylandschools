@echo off
REM Simple setup script for Joyland Schools Django project
REM This script handles Python environment setup and dependency installation

setlocal enabledelayedexpansion

echo.
echo ========================================
echo JOYLAND SCHOOLS - SETUP SCRIPT
echo ========================================
echo.

REM Step 1: Check and set execution policy for PowerShell
echo [STEP 1] Checking Python installation...
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python launcher (py) found
    py --version
) else (
    echo [ERROR] Python not found!
    echo.
    echo SOLUTION: Install Python from https://www.python.org/downloads/
    echo IMPORTANT: Check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo.
echo [STEP 2] Checking current directory...
cd /d C:\Users\STUDENT\Desktop\DATA\projects\joylandschools\backend
if %errorlevel% equ 0 (
    echo [OK] Changed to project directory
    echo Current: %cd%
) else (
    echo [ERROR] Could not change to project directory
    pause
    exit /b 1
)

echo.
echo [STEP 3] Checking virtual environment...
if exist ".venv\Scripts\python.exe" (
    echo [OK] Virtual environment found
) else (
    echo [INFO] Creating virtual environment...
    py -m venv .venv
    if %errorlevel% equ 0 (
        echo [OK] Virtual environment created
    ) else (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo.
echo [STEP 4] Activating virtual environment...
call .venv\Scripts\activate.bat
if %errorlevel% equ 0 (
    echo [OK] Virtual environment activated
    echo Prompt: !PROMPT!
) else (
    echo [WARNING] Could not activate, continuing with global Python
)

echo.
echo [STEP 5] Upgrading pip...
python -m pip install --upgrade pip setuptools wheel
if %errorlevel% neq 0 (
    echo [WARNING] pip upgrade had issues, continuing...
)

echo.
echo [STEP 6] Installing requirements...
if exist "requirements.txt" (
    echo [INFO] Installing requirements.txt...
    python -m pip install -r requirements.txt
    if %errorlevel% equ 0 (
        echo [OK] requirements.txt installed
    ) else (
        echo [ERROR] Failed to install requirements.txt
        pause
        exit /b 1
    )
) else (
    echo [WARNING] requirements.txt not found
)

if exist "requirements-dev.txt" (
    echo [INFO] Installing requirements-dev.txt...
    python -m pip install -r requirements-dev.txt
    if %errorlevel% equ 0 (
        echo [OK] requirements-dev.txt installed
    ) else (
        echo [WARNING] Failed to install requirements-dev.txt, continuing...
    )
)

echo.
echo [STEP 7] Checking Django...
python -m django --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Django installed
    python -m django --version
) else (
    echo [ERROR] Django not installed
    echo [INFO] Try: pip install Django
    pause
    exit /b 1
)

echo.
echo [STEP 8] Creating .env file...
if not exist ".env" (
    echo [INFO] Creating default .env file...
    (
        echo DEBUG=True
        echo SECRET_KEY=django-insecure-change-this-in-production
        echo ALLOWED_HOSTS=localhost,127.0.0.1
        echo OPENAI_API_KEY=your_openai_api_key_here
        echo CACHE_AI_RESULTS=True
        echo CACHE_BACKEND=django.core.cache.backends.locmem.LocMemCache
    ) > .env
    echo [OK] .env file created - EDIT WITH YOUR API KEY!
) else (
    echo [OK] .env file already exists
)

echo.
echo [STEP 9] Running migrations...
python manage.py migrate
if %errorlevel% equ 0 (
    echo [OK] Migrations completed
) else (
    echo [WARNING] Migration issues, continuing...
)

echo.
echo [STEP 10] Creating test teacher account...
(
    echo from django.contrib.auth import get_user_model
    echo User = get_user_model^(^)
    echo try:
    echo     teacher = User.objects.get^(username='teacher1'^)
    echo     print^(f"Teacher exists: {teacher.username}"^)
    echo except User.DoesNotExist:
    echo     teacher = User.objects.create_user^(
    echo         username='teacher1',
    echo         email='teacher1@joyland.edu',
    echo         password='testpass123',
    echo         role='teacher',
    echo         first_name='Demo',
    echo         last_name='Teacher'
    echo     ^)
    echo     print^(f"Teacher created: {teacher.username}"^)
    echo except Exception as e:
    echo     print^(f"Error: {e}"^)
) | python manage.py shell 2>nul
if %errorlevel% equ 0 (
    echo [OK] Test teacher account ready
)

echo.
echo ========================================
echo [SUCCESS] SETUP COMPLETE!
echo ========================================
echo.
echo NEXT STEPS:
echo 1. Edit .env file with your OpenAI API key
echo 2. Run: python manage.py runserver
echo 3. Open: http://127.0.0.1:8000/users/portal/login/
echo 4. Login: teacher1 / testpass123
echo.
echo COMMANDS:
echo   python manage.py runserver              - Start dev server
echo   python manage.py createsuperuser        - Create admin account
echo   python manage.py test users.tests.test_teacher_views  - Run tests
echo.
pause
