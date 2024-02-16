@echo off
where /q python
if %ERRORLEVEL% neq 0 (
    echo Python is not installed. Please install Python and try again.
    exit /b
)
if not exist PyReversi.py (
    echo PyReversi.py does not exist. Please check the file path and try again.
    exit /b
)
python PyReversi.py
