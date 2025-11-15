# Development Setup

## Initial Setup

1. Create and activate a virtual environment:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # PowerShell
```

2. Install dependencies:
```powershell
pip install -r requirements.txt
pip install -r requirements-dev.txt  # for development tools
```

3. Initialize the database:
```powershell
python manage.py migrate
python manage.py createsuperuser  # follow prompts
```

## Running the Development Server

This project includes a PowerShell script to start the dev server bound to 0.0.0.0 so it's accessible to LAN devices.

1. From the repository root:
```powershell
cd backend
.\.venv\Scripts\Activate.ps1  # if not already activated
```

2. Start the server:
```powershell
# Using the helper script (recommended):
.\dev.ps1 -Host 0.0.0.0 -Port 8000

# Or directly:
python manage.py runserver 0.0.0.0:8000
```

## Development Tools

1. Run tests:
```powershell
pytest  # run all tests
pytest users/tests/  # run specific test directory
```

2. Code formatting and linting:
```powershell
# Format code
black .

# Run linter
ruff .
```

## Environment Variables

The following can be set in a `.env` file or environment:

- `DJANGO_SECRET_KEY`: Secret key (required in production)
- `DJANGO_DEBUG`: Set to "1" or "true" to enable debug mode
- `DJANGO_LOG_LEVEL`: Set logging level (default: INFO)
- `SITE_DOMAIN`: Your site's domain (default: localhost:8000)

OpenAI Integration:
- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_DEFAULT_MODEL`: Default model to use (default: gpt-4)
- `ENABLE_GPT5_MINI`: Set to "1" or "true" to use GPT-5 mini model

## Important Notes

- Ensure your firewall allows connections if you want LAN access
- The dev server auto-reloads on code changes
- Never use the dev server in production
- Logs are written to `logs/joyland.log`
- Run tests before committing changes
