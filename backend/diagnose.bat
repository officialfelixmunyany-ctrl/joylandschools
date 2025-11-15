@echo off
REM Diagnostic script to check Python installation and PATH

echo ========================================
echo PYTHON ENVIRONMENT DIAGNOSTIC
echo ========================================
echo.

REM Check if python is in PATH
echo [1] Checking if python is accessible...
where python
if %errorlevel% equ 0 (
    echo ^✓ Python found in PATH
    python --version
) else (
    echo ^✗ Python NOT found in PATH
)
echo.

REM Check if py launcher is available
echo [2] Checking if py launcher is available...
where py
if %errorlevel% equ 0 (
    echo ^✓ Python launcher (py) found
    py --version
) else (
    echo ^✗ Python launcher (py) NOT found
)
echo.

REM Check common Python installation paths
echo [3] Checking common Python installation paths...
if exist "C:\Python311\python.exe" (
    echo ^✓ Found Python 3.11 at C:\Python311
    C:\Python311\python.exe --version
) else (
    echo ^✗ C:\Python311 not found
)

if exist "C:\Python310\python.exe" (
    echo ^✓ Found Python 3.10 at C:\Python310
    C:\Python310\python.exe --version
) else (
    echo ^✗ C:\Python310 not found
)

if exist "C:\Program Files\Python311\python.exe" (
    echo ^✓ Found Python 3.11 at Program Files
    "C:\Program Files\Python311\python.exe" --version
) else (
    echo ^✗ Program Files\Python311 not found
)

if exist "C:\Program Files\Python310\python.exe" (
    echo ^✓ Found Python 3.10 at Program Files
    "C:\Program Files\Python310\python.exe" --version
) else (
    echo ^✗ Program Files\Python310 not found
)
echo.

REM Check AppData local Python
echo [4] Checking AppData local Python...
if exist "%APPDATA%\Python\Python311\Scripts" (
    echo ^✓ Found Python Scripts in AppData
) else (
    echo ^✗ AppData Python Scripts not found
)
echo.

REM Display PATH
echo [5] Current PATH environment variable:
echo %PATH%
echo.

echo ========================================
echo DIAGNOSTICS COMPLETE
echo ========================================
