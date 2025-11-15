# PowerShell diagnostic and setup script for Django project

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "JOYLAND SCHOOLS - ENVIRONMENT SETUP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Color helpers
function Write-Success { Write-Host "✓ $args" -ForegroundColor Green }
function Write-Error { Write-Host "✗ $args" -ForegroundColor Red }
function Write-Info { Write-Host "ℹ $args" -ForegroundColor Blue }
function Write-Warning { Write-Host "⚠ $args" -ForegroundColor Yellow }

Write-Info "Step 1: Setting execution policy..."
try {
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    Write-Success "Execution policy set to RemoteSigned"
} catch {
    Write-Error "Failed to set execution policy: $_"
}
Write-Host ""

Write-Info "Step 2: Locating Python..."
$pythonPaths = @(
    "C:\Python311\python.exe",
    "C:\Python310\python.exe",
    "C:\Program Files\Python311\python.exe",
    "C:\Program Files\Python310\python.exe"
)

$pythonExe = $null
foreach ($path in $pythonPaths) {
    if (Test-Path $path) {
        Write-Success "Found Python at: $path"
        $pythonExe = $path
        & $pythonExe --version
        break
    }
}

if (-not $pythonExe) {
    Write-Error "Python not found in common locations!"
    Write-Warning "Trying 'py' launcher..."
    try {
        $pyVersion = & py --version
        Write-Success "Python launcher found: $pyVersion"
        $pythonExe = "py"
    } catch {
        Write-Error "Python not found on system!"
        Write-Info "Please install Python from https://www.python.org/downloads/"
        Write-Info "Make sure to check 'Add Python to PATH' during installation"
        exit 1
    }
}
Write-Host ""

Write-Info "Step 3: Checking current directory..."
$projectPath = "C:\Users\STUDENT\Desktop\DATA\projects\joylandschools\backend"
if (Test-Path $projectPath) {
    Write-Success "Project path confirmed: $projectPath"
    Set-Location $projectPath
} else {
    Write-Error "Project path not found: $projectPath"
    exit 1
}
Write-Host ""

Write-Info "Step 4: Checking virtual environment..."
$venvPath = ".\.venv"
if (Test-Path "$venvPath\Scripts\python.exe") {
    Write-Success "Virtual environment found at: $venvPath"
    $venvActive = $true
} else {
    Write-Warning "Virtual environment not found. Creating one..."
    try {
        & $pythonExe -m venv .venv
        Write-Success "Virtual environment created"
        $venvActive = $true
    } catch {
        Write-Error "Failed to create virtual environment: $_"
        exit 1
    }
}
Write-Host ""

Write-Info "Step 5: Activating virtual environment..."
try {
    & ".\venv\Scripts\Activate.ps1"
    Write-Success "Virtual environment activated"
} catch {
    Write-Error "Failed to activate virtual environment: $_"
    Write-Info "Trying alternative activation method..."
    $env:PATH = ".\venv\Scripts;$env:PATH"
    Write-Warning "Using PATH modification instead"
}
Write-Host ""

Write-Info "Step 6: Installing dependencies..."
try {
    & python -m pip install --upgrade pip setuptools wheel
    Write-Success "pip upgraded"
    
    if (Test-Path "requirements.txt") {
        & python -m pip install -r requirements.txt
        Write-Success "requirements.txt installed"
    } else {
        Write-Warning "requirements.txt not found"
    }
    
    if (Test-Path "requirements-dev.txt") {
        & python -m pip install -r requirements-dev.txt
        Write-Success "requirements-dev.txt installed"
    } else {
        Write-Warning "requirements-dev.txt not found"
    }
} catch {
    Write-Error "Failed to install dependencies: $_"
    exit 1
}
Write-Host ""

Write-Info "Step 7: Checking Django installation..."
try {
    & python -m django --version
    Write-Success "Django is installed"
} catch {
    Write-Error "Django not found: $_"
    exit 1
}
Write-Host ""

Write-Info "Step 8: Creating .env file (if not exists)..."
$envFile = ".env"
if (-not (Test-Path $envFile)) {
    Write-Warning "Creating default .env file..."
    $envContent = @"
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# OpenAI Settings
OPENAI_API_KEY=your_openai_api_key_here

# Cache Settings
CACHE_AI_RESULTS=True
CACHE_BACKEND=django.core.cache.backends.locmem.LocMemCache

# Database (defaults to SQLite)
DATABASE_URL=sqlite:///db.sqlite3
"@
    Set-Content -Path $envFile -Value $envContent
    Write-Success ".env file created - EDIT IT WITH YOUR API KEY!"
} else {
    Write-Success ".env file already exists"
}
Write-Host ""

Write-Info "Step 9: Running Django migrations..."
try {
    & python manage.py migrate
    Write-Success "Migrations completed"
} catch {
    Write-Error "Migration failed: $_"
}
Write-Host ""

Write-Info "Step 10: Creating test teacher account..."
$createTeacher = @"
from django.contrib.auth import get_user_model
User = get_user_model()

try:
    teacher = User.objects.get(username='teacher1')
    print(f"Teacher already exists: {teacher.username}")
except User.DoesNotExist:
    teacher = User.objects.create_user(
        username='teacher1',
        email='teacher1@joyland.edu',
        password='testpass123',
        role='teacher',
        first_name='Demo',
        last_name='Teacher'
    )
    print(f"Teacher created: {teacher.username}")
except Exception as e:
    print(f"Error: {e}")
"@

try {
    Write-Info "Executing: python manage.py shell"
    $createTeacher | & python manage.py shell
    Write-Success "Test teacher account setup complete"
} catch {
    Write-Warning "Could not create test teacher automatically: $_"
    Write-Info "You can create it manually in the Django shell later"
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ SETUP COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit the .env file with your OpenAI API key"
Write-Host "2. Run: python manage.py runserver"
Write-Host "3. Open browser: http://127.0.0.1:8000/users/portal/login/"
Write-Host "4. Login with: teacher1 / testpass123"
Write-Host ""
Write-Host "Commands:" -ForegroundColor Yellow
Write-Host "  python manage.py runserver    # Start development server"
Write-Host "  python manage.py createsuperuser  # Create admin account"
Write-Host "  python manage.py test users.tests.test_teacher_views  # Run tests"
Write-Host ""
