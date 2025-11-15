# Project Refactoring Guide

## Overview

This guide walks through a comprehensive refactoring of the Joyland Schools project to improve structure, maintainability, and follow Django best practices.

**Status:** Using automation script for Phases 1–4, with detailed manual steps for model/view splitting.

---

## Quick Start

### Using the Automation Script

```powershell
# Preview all changes (safe dry-run)
python refactor_project.py --dry-run

# Run refactoring (creates backups automatically)
python refactor_project.py

# Run only Phase 1 (documentation)
python refactor_project.py --phase 1
```

Backups are saved to `.refactor_backups/[timestamp]/` for safety.

---

## Phase 1: Move Documentation

### What It Does
Moves all `.md` files from `backend/` root to `backend/docs/`.

### Files Moved
- `README.md`
- `README_DEV.md`, `README_NEW.md`, `README_SETUP.md`
- `QUICK_START_MANUAL.md`
- `PYTHON_INSTALLATION_FIX.md`
- `ORGANIC_BACKGROUND_GUIDE.md`
- `FINAL_SUMMARY.md`, `DOCUMENTATION_INDEX.md`
- `TEACHER_PORTAL_GUIDE.md`, `THEME_DOCUMENTATION.md`

### Automated By
Script Phase 1: `refactor_project.py --phase 1`

### Manual Fallback (if script fails)
```powershell
# In backend folder
mkdir docs
Move-Item README.md docs/
Move-Item README_DEV.md docs/
# ... repeat for each .md file
```

---

## Phase 2: Create Core App

### What It Does
Creates a new Django app called `core` for non-authentication content (announcements, events, registration, presence tracking).

### Automated By
Script Phase 2: `refactor_project.py --phase 2`

### Manual Equivalent
```powershell
cd backend
python manage.py startapp core
```

### Verify
```powershell
# Should create:
# - core/__init__.py
# - core/admin.py
# - core/apps.py
# - core/models.py
# - core/tests.py
# - core/views.py
# - core/migrations/
```

---

## Phase 3: Split Models (Manual)

### What It Does
Moves Announcement, Event, RegistrationRequest, Presence, DailyPresence models from `users/models.py` to `core/models.py`.

### Why
- **users** app should focus only on authentication (User, StudentProfile)
- **core** app handles site-wide content (announcements, events, etc.)
- Better separation of concerns

### Step-by-Step

#### Step 3a: Backup Current Files
```powershell
# Backup users models (automatic if using script)
Copy-Item users/models.py users/models.py.backup
Copy-Item core/models.py core/models.py.backup
```

#### Step 3b: Extract Models from users/models.py

1. Open `users/models.py`
2. Identify and **copy** these class definitions:
   - `AnnouncementManager` (class)
   - `Announcement` (model)
   - `EventManager` (class)
   - `Event` (model)
   - `RegistrationRequest` (model)
   - `Presence` (model)
   - `DailyPresence` (model)

3. Keep in `users/models.py`:
   - Imports
   - `User` model
   - `StudentProfile` model

#### Step 3c: Paste Models into core/models.py

1. Open `core/models.py`
2. Add imports at the top:
   ```python
   from django.db import models
   from django.utils import timezone
   from django.core.cache import cache
   ```

3. Paste the extracted model classes

4. Update any imports that reference `users` models:
   ```python
   # If Event references User or StudentProfile:
   from users.models import User, StudentProfile
   ```

#### Step 3d: Update Imports in users/models.py

1. Remove the model definitions (but keep User, StudentProfile, etc.)
2. Add imports for models that are now in core:
   ```python
   from core.models import Announcement, Event, RegistrationRequest, Presence, DailyPresence
   
   # If users/views.py or users/admin.py import these, they'll now import from core
   ```

#### Step 3e: Update users/admin.py

Replace:
```python
from users.models import Announcement, Event, RegistrationRequest
```

With:
```python
from core.models import Announcement, Event, RegistrationRequest
```

#### Step 3f: Update joyland/settings.py

Add `'core'` to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # ... other apps ...
    'users',
    'core',  # Add this
]
```

---

## Phase 4: Move Views (Manual)

### What It Does
Moves view modules from `users/views/` to `core/views/` and updates imports.

### Files to Move
- `users/views/announcements.py` → `core/views/announcements.py`
- `users/views/registration.py` → `core/views/registration.py` (if exists)

### Step-by-Step

#### Step 4a: Create core/views/ Directory
```powershell
mkdir core/views
```

#### Step 4b: Create core/views/__init__.py
```python
from .announcements import *
# from .registration import *  # if it exists
```

#### Step 4c: Move View Files
```powershell
# Copy files first
Copy-Item users/views/announcements.py core/views/announcements.py
Copy-Item users/views/registration.py core/views/registration.py

# Then delete originals (after testing)
Remove-Item users/views/announcements.py
Remove-Item users/views/registration.py
```

#### Step 4d: Create core/urls.py

```python
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Announcements
    path('announcements/', views.announcements, name='announcements'),
    path('announcements/archive/', views.announcements_archive, name='announcements_archive'),
    # Add other core URLs here
]
```

#### Step 4e: Update joyland/urls.py

Add the core app URLs:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('core.urls')),  # Add this
]
```

#### Step 4f: Update Any Existing URL References

In templates and views, if you reference URLs like `{% url 'announcements' %}`, they now live in the `core` app:

```html
<!-- Old -->
{% url 'announcements' %}

<!-- New -->
{% url 'core:announcements' %}
```

---

## Phase 5: Move Templates (Manual)

### What It Does
Organizes templates by app. Core-related templates move to `templates/core/`.

### Files to Move
```
templates/
├── announcements.html              → templates/core/announcements.html
├── announcements_archive.html      → templates/core/announcements_archive.html
├── includes/
│   ├── announcements.html          → templates/core/includes/announcements.html
│   ├── announcements_list.html     → templates/core/includes/announcements_list.html
│   ├── announcement_form.html      → templates/core/includes/announcement_form.html
│   ├── announcement_confirm_delete.html → templates/core/includes/announcement_confirm_delete.html
│   └── events_preview.html         → templates/core/includes/events_preview.html
```

### Step-by-Step

#### Step 5a: Create Template Directories
```powershell
mkdir templates/core
mkdir templates/core/includes
```

#### Step 5b: Move Templates
```powershell
Move-Item templates/announcements.html templates/core/
Move-Item templates/announcements_archive.html templates/core/
Move-Item templates/includes/announcements.html templates/core/includes/
# ... etc.
```

#### Step 5c: Update Template Includes

In `templates/landing.html`, update:
```html
<!-- Old -->
{% include 'includes/announcements.html' %}
{% include 'includes/events_preview.html' %}

<!-- New -->
{% include 'core/includes/announcements.html' %}
{% include 'core/includes/events_preview.html' %}
```

In any admin templates or forms that reference these includes, update paths similarly.

---

## Phase 6: Consolidate JavaScript (Automated)

### What It Does
Combines multiple JavaScript files into a single `static/js/main.js` for better performance.

### Files Consolidated
- `animations.js`
- `hero-status.js`
- `hero-transition.js`
- `landing-carousel.js`
- `navbar-hover.js`

### Automated By
Script Phase 4: `refactor_project.py --phase 4`

### Manual Equivalent
1. Create `static/js/main.js`
2. Copy content from each file, in order, separated by comments:
   ```javascript
   // ===== animations.js =====
   // [content of animations.js]
   
   // ===== hero-status.js =====
   // [content of hero-status.js]
   
   // ... etc.
   ```

### Step 6a: Update base.html

Replace multiple script tags:
```html
<!-- Old -->
<script src="{% static 'js/animations.js' %}"></script>
<script src="{% static 'js/hero-status.js' %}"></script>
<script src="{% static 'js/hero-transition.js' %}"></script>
<script src="{% static 'js/landing-carousel.js' %}"></script>
<script src="{% static 'js/navbar-hover.js' %}"></script>

<!-- New -->
<script src="{% static 'js/main.js' %}"></script>
```

### Step 6b: Delete Individual JS Files (Optional)
```powershell
# After verifying everything works
Remove-Item static/js/animations.js
Remove-Item static/js/hero-status.js
Remove-Item static/js/hero-transition.js
Remove-Item static/js/landing-carousel.js
Remove-Item static/js/navbar-hover.js
```

---

## Phase 7: Remove views.py / views/ Conflict (Manual)

### What It Does
Ensures `users/views.py` doesn't conflict with `users/views/` directory.

### Step-by-Step

#### Step 7a: Check if users/views.py Exists
```powershell
ls users/views.py
# If it exists and has code, back it up
```

#### Step 7b: If users/views.py Has Code
1. Copy code to `users/views/__init__.py` or relevant modules
2. Delete `users/views.py`
3. Verify imports still work

#### Step 7c: Verify users/views/__init__.py

```python
from .base import *  # or whatever modules exist
from .auth import *  # etc.

# Avoid import conflicts by being explicit
__all__ = ['LoginView', 'RegisterView', 'LogoutView', 'ProfileView', 'StudentProfileView']
```

---

## Phase 8: Run Migrations

### Create Migration for Core App
```powershell
cd backend
python manage.py makemigrations core
```

### Apply Migrations
```powershell
python manage.py migrate
```

---

## Phase 9: Run Tests

### Full Test Suite
```powershell
python manage.py test
```

### Specific Tests
```powershell
# Test auth flows
python manage.py test users.tests.test_auth_flow

# Test core (if migrations created models)
python manage.py test core
```

### Expected Output
```
Found X test(s)...
Ran X tests in XXs
OK
```

---

## Rollback Instructions

If something goes wrong, backups are saved in `.refactor_backups/[timestamp]/`.

### Manual Rollback
```powershell
# List backups
ls .refactor_backups/

# Restore from specific backup
copy .refactor_backups/20250114_152030/users/models.py users/models.py
# ... repeat for each changed file
```

---

## Checklist

After completing all phases:

- [ ] Phase 1: Documentation moved to `docs/`
- [ ] Phase 2: Core app created with `manage.py startapp core`
- [ ] Phase 3: Models split — Announcement, Event, etc. moved to `core/models.py`
- [ ] Phase 4: Views moved — `announcements.py`, `registration.py` moved to `core/views/`
- [ ] Phase 4b: `core/urls.py` created and wired to `joyland/urls.py`
- [ ] Phase 5: Templates moved to `templates/core/`
- [ ] Phase 5b: Template includes updated in landing.html and other files
- [ ] Phase 6: JavaScript consolidated into `main.js`
- [ ] Phase 6b: `base.html` updated to use single `main.js`
- [ ] Phase 7: `users/views.py` / `users/views/` conflict resolved
- [ ] Phase 8: Migrations created and applied (`migrate`)
- [ ] Phase 9: All tests passing

---

## Troubleshooting

### "migrate: No migrations to apply"
**Cause:** Core app models not properly defined or already migrated.
**Fix:** Run `python manage.py makemigrations core` again, then `migrate`.

### "ModuleNotFoundError: No module named 'core'"
**Cause:** Core app not added to `INSTALLED_APPS` in settings.py.
**Fix:** Edit `joyland/settings.py` and add `'core'` to the list.

### "ImportError: cannot import name 'Announcement' from 'users.models'"
**Cause:** Model already moved to core, but old import still used.
**Fix:** Update imports: `from core.models import Announcement`.

### JavaScript doesn't work after consolidation
**Cause:** Function or variable name collisions in combined main.js.
**Fix:** Review combined file for duplicate function names; wrap sections in IIFE or modules.

### Tests fail after refactoring
**Cause:** Old import paths or missing app URLs.
**Fix:** 
1. Update import paths in tests: `from core.models import Announcement`
2. Verify `core` is in `INSTALLED_APPS`
3. Check URL configuration in `joyland/urls.py`

---

## Performance Impact

After refactoring:
- **HTTP requests:** Reduced by 1–4 (fewer individual JS files)
- **Page load time:** Likely 50–100ms faster (fewer file lookups)
- **Code maintainability:** Significantly improved (models, views, templates organized by feature)
- **Cache performance:** Improved caching due to smaller, focused modules

---

## Future Improvements

Phase 2 items (after this refactoring):

1. **Add core API:** REST endpoints for announcements/events via Django REST Framework
2. **WebSocket support:** Real-time presence updates using Django Channels
3. **Admin customization:** Create `core/admin.py` with advanced filters and bulk actions
4. **Testing:** Add comprehensive tests for core models and views
5. **Documentation:** Add docstrings to all core models and views

---

**Last Updated:** 2025-01-14
