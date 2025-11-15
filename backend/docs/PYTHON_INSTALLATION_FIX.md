# CRITICAL: Python Not Found - Complete Solution

## ROOT CAUSE
Your system doesn't have Python installed or it's not accessible in the Windows PATH environment variable.

## Evidence from Your Terminal
```
python : The term 'python' is not recognized as a command
pip : The term 'pip' is not recognized as a command
No installed Python found!
```

---

## ✅ SOLUTION: Install Python

### Step 1: Download Python
1. Go to https://www.python.org/downloads/
2. Download **Python 3.11** (or 3.10+)
3. Choose the installer matching your Windows version (32-bit or 64-bit)

### Step 2: Install Python (CRITICAL STEPS)
1. Run the installer
2. **CHECK THIS BOX:** ☑️ "Add Python 3.11 to PATH"
3. Check "Install pip"
4. Choose "Install Now" or customize to include:
   - ✅ Python core
   - ✅ pip (package installer)
   - ✅ Python documentation
5. Click "Install"
6. When done, click "Disable path length limit" (optional but recommended)

### Step 3: Verify Installation
After installation, **close and reopen PowerShell**, then run:

```powershell
python --version
pip --version
py --version
```

All three should work. If they do, proceed to Step 4.

### Step 4: Navigate to Project
```powershell
cd C:\Users\STUDENT\Desktop\DATA\projects\joylandschools\backend
```

### Step 5: Create Virtual Environment
```powershell
python -m venv .venv
```

### Step 6: Activate Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```

If you get an error about execution policy, run this FIRST:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

Then activate again.

### Step 7: Install Dependencies
```powershell
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Step 8: Create .env File
Create a file named `.env` in the `backend` folder with:
```
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
OPENAI_API_KEY=your_openai_api_key_here
CACHE_AI_RESULTS=True
```

### Step 9: Run Migrations
```powershell
python manage.py migrate
```

### Step 10: Start Django Server
```powershell
python manage.py runserver
```

Expected output:
```
Starting development server at http://127.0.0.1:8000/
```

---

## 🔍 TROUBLESHOOTING: If Python Still Not Found

### Option A: Use Full Python Path
If Python is installed but not in PATH, use the full path:

```powershell
# Instead of: python manage.py runserver
# Use:
C:\Users\YourUsername\AppData\Local\Programs\Python\Python311\python.exe manage.py runserver
```

To find your Python path:
1. Open Command Prompt (not PowerShell)
2. Type: `python --version`
3. If it works, get the path: `where python`

### Option B: Check if Python Exists
In PowerShell, run:
```powershell
Get-Command python
Get-Command pip
Get-Command py
```

If any show a path, Python is installed. Use that path.

### Option C: Use Python Launcher
If `py` works, use it instead:
```powershell
py -m venv .venv
py -m pip install -r requirements.txt
py manage.py runserver
```

### Option D: Reinstall Python
If nothing works:
1. Open Control Panel → Programs → Programs and Features
2. Find "Python 3.x"
3. Click "Uninstall"
4. Go back to Step 1: Download and reinstall
5. **CRITICAL:** Check "Add Python to PATH"

---

## 📋 COMPLETE QUICK START (After Python Installed)

```powershell
# 1. Navigate to project
cd C:\Users\STUDENT\Desktop\DATA\projects\joylandschools\backend

# 2. Set execution policy (one-time)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# 3. Create virtual environment
python -m venv .venv

# 4. Activate it
.\.venv\Scripts\Activate.ps1

# 5. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 6. Create .env file (edit with your OpenAI API key)
echo "DEBUG=True`nOPENAI_API_KEY=your_key_here" > .env

# 7. Run migrations
python manage.py migrate

# 8. Start server
python manage.py runserver

# 9. Open browser
# http://127.0.0.1:8000/users/portal/login/
# Login: teacher1 / testpass123
```

---

## ✨ After Python Installation

Once Python is properly installed and in PATH:

1. Open PowerShell
2. Run the quick start commands above
3. Access the portal at http://127.0.0.1:8000/users/portal/login/
4. Enjoy the AI-powered teacher dashboard!

---

## 📞 Still Having Issues?

If Python still won't work:
1. Screenshot the error
2. Verify Python is installed: Check "C:\Program Files" or "C:\Users\[YourName]\AppData\Local\Programs\Python"
3. Try using Command Prompt instead of PowerShell
4. Consider using VS Code's Python extension to manage environments

---

**Key Point:** The #1 issue is that Python is not installed or not in PATH. Installing Python correctly solves 99% of the problems you're experiencing.
