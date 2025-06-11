@echo off
REM VFS Global Appointment Bot - Windows Setup Script

echo 🚀 VFS Global Appointment Bot - Quick Setup
echo ===========================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.7+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not installed. Please install pip first.
    pause
    exit /b 1
)

echo ✅ pip found
pip --version

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv vfs_bot_env

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call vfs_bot_env\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📥 Installing Python packages...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo ⚙️ Creating configuration file...
    copy .env.example .env
    echo 📝 Please edit .env file with your VFS Global credentials
) else (
    echo ⚙️ Configuration file already exists
)

REM Create necessary directories
echo 📁 Creating directories...
if not exist logs mkdir logs
if not exist screenshots mkdir screenshots

REM Check if Chrome is installed
where chrome >nul 2>&1
if %errorlevel% neq 0 (
    where "C:\Program Files\Google\Chrome\Application\chrome.exe" >nul 2>&1
    if %errorlevel% neq 0 (
        where "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" >nul 2>&1
        if %errorlevel% neq 0 (
            echo ⚠️ Google Chrome not found. Please install Chrome manually.
            echo Download from: https://www.google.com/chrome/
        ) else (
            echo ✅ Google Chrome found
        )
    ) else (
        echo ✅ Google Chrome found
    )
) else (
    echo ✅ Google Chrome found
)

echo.
echo 🎉 Setup completed successfully!
echo.
echo Next steps:
echo 1. Edit .env file with your VFS Global credentials:
echo    notepad .env
echo.
echo 2. Run the bot:
echo    vfs_bot_env\Scripts\activate.bat
echo    python main.py
echo.
echo 📖 For detailed instructions, see INSTALLATION_GUIDE.md
echo.
echo ⚠️ Important: This bot is for educational purposes only.
echo    Please ensure compliance with VFS Global's terms of service.
echo.
pause

