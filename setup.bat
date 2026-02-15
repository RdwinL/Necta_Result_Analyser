@echo off
REM NECTA Analysis Dashboard - Windows Setup Script

echo ==================================================
echo NECTA Form 4 Results Analysis Dashboard - Setup
echo ==================================================
echo.

REM Check Python version
echo Checking Python version...
python --version 2>NUL
if errorlevel 1 (
    echo X Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo.
echo Installing required packages...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ==================================================
    echo Installation completed successfully!
    echo ==================================================
    echo.
    echo To start the application, run:
    echo   streamlit run necta_analysis_app.py
    echo.
    echo The dashboard will open automatically in your browser at:
    echo   http://localhost:8501
    echo.
    echo Features:
    echo   - Analyze NECTA Form 4 results
    echo   - View top performing schools
    echo   - Regional performance analysis
    echo   - Subject-wise comparisons
    echo   - Download data in CSV/Excel format
    echo.
    echo ==================================================
) else (
    echo.
    echo X Installation failed
    echo Please check error messages above and try again
    pause
    exit /b 1
)

pause
