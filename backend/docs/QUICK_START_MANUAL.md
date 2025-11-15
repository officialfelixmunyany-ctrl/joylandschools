# 🚀 MANUAL SETUP GUIDE - Step by Step

**Current Issue:** Python is not installed or not in your Windows PATH

---

## IMMEDIATE ACTION REQUIRED

### Step 1: Verify If Python Is Installed

**Option A: Command Prompt (Recommended)**
1. Press `Win + R`
2. Type: `cmd`
3. Press Enter
4. In Command Prompt, type: `python --version`

**What you should see:**
```
Python 3.11.x
```

**If you see this error:**
```
'python' is not recognized as an internal or external command
```
→ Go to **SECTION A: Install Python** below

---

## SECTION A: INSTALL PYTHON (if not installed)

### Step 1: Download Python
1. Visit: https://www.python.org/downloads/
2. Click the big yellow button: **"Download Python 3.11.X"**
3. Choose your Windows version (32-bit or 64-bit)
   - Most modern Windows is 64-bit
   - File will be about 100MB
4. Double-click the installer when downloaded

### Step 2: Install Python - CRITICAL STEPS

**When installer opens:**

1. **Check this box FIRST:** 
   - ☑️ "Add Python 3.11 to PATH"
   
2. Click: **"Install Now"**

3. Wait for installation (about 2-3 minutes)

4. You should see: "Setup was successful"

5. **CLOSE Command Prompt if open** (completely)

---

## SECTION B: VERIFY PYTHON INSTALLATION

### Step 1: Test Python
1. Press `Win + R`
2. Type: `cmd`
3. Press Enter
4. In Command Prompt, run these commands:

```cmd
python --version
pip --version
py --version
```

**Expected output for all three:**
```
Python 3.11.x
pip version ...
```

**If all three work** → Proceed to **SECTION C**

**If any fail** → Python not properly installed. Uninstall and try again. Make sure to check "Add Python to PATH"

---

## SECTION C: SETUP PROJECT (in Command Prompt, NOT PowerShell)

### Step 1: Navigate to Project
```cmd
cd C:\Users\STUDENT\Desktop\DATA\projects\joylandschools\backend
```

### Step 2: Create Virtual Environment
```cmd
python -m venv .venv
```

Wait 1-2 minutes. You'll see no output, which is normal.

### Step 3: Activate Virtual Environment
```cmd
.venv\Scripts\activate.bat
```

**You should see** `(.venv)` at the start of your command prompt line:
```
(.venv) C:\Users\STUDENT\Desktop\DATA\projects\joylandschools\backend>
```

### Step 4: Upgrade pip
```cmd
python -m pip install --upgrade pip
```

### Step 5: Install Dependencies
```cmd
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

**This will take 3-5 minutes.** You'll see packages installing. When done, you'll see:
```
Successfully installed ...
```

### Step 6: Create .env File
Using Notepad or your editor, create a file called `.env` in the `backend` folder with:

```
DEBUG=True
SECRET_KEY=django-insecure-change-me-in-production
ALLOWED_HOSTS=localhost,127.0.0.1
OPENAI_API_KEY=your_openai_api_key_here
CACHE_AI_RESULTS=True
CACHE_BACKEND=django.core.cache.backends.locmem.LocMemCache
```

**Save it** in: `C:\Users\STUDENT\Desktop\DATA\projects\joylandschools\backend\.env`

### Step 7: Run Migrations
```cmd
python manage.py migrate
```

You'll see:
```
Operations to perform:
  Apply all migrations: admin, auth, ...
Running migrations:
  Applying ... OK
  ...
```

### Step 8: Create Test Teacher
```cmd
python manage.py shell
```

You're now in Python shell. Type:

```python
from users.models import User

User.objects.create_user(
    username='teacher1',
    email='teacher1@joyland.edu',
    password='testpass123',
    role='teacher',
    first_name='Demo',
    last_name='Teacher'
)

exit()
```

---

## SECTION D: RUN THE PORTAL

### Step 1: Start Django Server (in Command Prompt with venv activated)
```cmd
python manage.py runserver
```

**You should see:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Step 2: Open Browser
Go to: **http://127.0.0.1:8000/users/portal/login/**

### Step 3: Login
```
Username: teacher1
Password: testpass123
```

### Step 4: View Dashboard
You should see the teacher dashboard at:
```
http://127.0.0.1:8000/users/portal/teacher/
```

---

## SECTION E: STOP THE SERVER

Press: `Ctrl + C` in Command Prompt

The server stops immediately.

---

## SECTION F: RUN AGAIN NEXT TIME

Simply do:

```cmd
cd C:\Users\STUDENT\Desktop\DATA\projects\joylandschools\backend
.venv\Scripts\activate.bat
python manage.py runserver
```

Then open: http://127.0.0.1:8000/users/portal/login/

---

## TROUBLESHOOTING

### Q: "python command not found"
**A:** Python not installed or not in PATH
- Follow **SECTION A** again, making sure to check "Add Python to PATH"

### Q: "pip command not found"
**A:** pip not installed with Python
- Reinstall Python, making sure pip is selected during installation

### Q: "ModuleNotFoundError" when running server
**A:** Dependencies not installed
- Run: `pip install -r requirements.txt`

### Q: "Port 8000 already in use"
**A:** Another Django server is running
- Find it: `netstat -ano | findstr :8000`
- Kill it or use different port: `python manage.py runserver 8001`

### Q: ".env not being read"
**A:** Restart Django server after creating .env file

### Q: "Database error"
**A:** Migrations not run
- Run: `python manage.py migrate`

---

## KEY DIFFERENCES: Command Prompt vs PowerShell

Use **Command Prompt (cmd)** NOT PowerShell for this project:

| Action | Command Prompt | PowerShell |
|--------|---|---|
| Activate venv | `.venv\Scripts\activate.bat` | `.\.venv\Scripts\Activate.ps1` |
| Run server | `python manage.py runserver` | Same |
| Stop server | `Ctrl + C` | Same |

---

## SUMMARY: ONE-TIME SETUP

```
1. Install Python 3.11+
2. Close Command Prompt completely
3. Open NEW Command Prompt
4. cd C:\Users\STUDENT\Desktop\DATA\projects\joylandschools\backend
5. python -m venv .venv
6. .venv\Scripts\activate.bat
7. pip install -r requirements.txt
8. pip install -r requirements-dev.txt
9. Create .env file with OPENAI_API_KEY
10. python manage.py migrate
11. python manage.py shell (create teacher) → exit()
12. python manage.py runserver
13. Open: http://127.0.0.1:8000/users/portal/login/
14. Login: teacher1 / testpass123
```

**Then you can use the AI-powered teacher dashboard!**

---

## NEXT STEPS AFTER SETUP

✅ The teacher portal is ready with:
- Term planning (AI-powered)
- Assessment generation
- Student progress analysis
- Differentiated activities
- Full caching support
- Loading indicators

Edit `.env` with your OpenAI API key to start using AI features.

---

**Questions?** Check the full guide at: `TEACHER_PORTAL_GUIDE.md`
