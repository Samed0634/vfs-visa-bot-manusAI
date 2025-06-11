#!/bin/bash

# VFS Global Appointment Bot - Quick Setup Script
# This script automates the initial setup process

set -e

echo "🚀 VFS Global Appointment Bot - Quick Setup"
echo "==========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip found: $(pip3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv vfs_bot_env

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source vfs_bot_env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing Python packages..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️ Creating configuration file..."
    cp .env.example .env
    echo "📝 Please edit .env file with your VFS Global credentials"
else
    echo "⚙️ Configuration file already exists"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs screenshots

# Check if Chrome is installed
if command -v google-chrome &> /dev/null; then
    echo "✅ Google Chrome found: $(google-chrome --version)"
elif command -v chromium-browser &> /dev/null; then
    echo "✅ Chromium found: $(chromium-browser --version)"
else
    echo "⚠️ Google Chrome not found. Installing..."
    
    # Detect OS and install Chrome
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            # Debian/Ubuntu
            wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
            sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
            sudo apt-get update
            sudo apt-get install -y google-chrome-stable
        elif command -v yum &> /dev/null; then
            # CentOS/RHEL
            sudo yum install -y wget
            wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
            sudo yum localinstall -y google-chrome-stable_current_x86_64.rpm
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install --cask google-chrome
        else
            echo "❌ Please install Google Chrome manually from https://www.google.com/chrome/"
            exit 1
        fi
    else
        echo "❌ Unsupported OS. Please install Google Chrome manually."
        exit 1
    fi
fi

# Make main.py executable
chmod +x main.py

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your VFS Global credentials:"
echo "   nano .env"
echo ""
echo "2. Run the bot:"
echo "   source vfs_bot_env/bin/activate"
echo "   python main.py"
echo ""
echo "3. For Docker deployment:"
echo "   docker-compose up -d"
echo ""
echo "📖 For detailed instructions, see INSTALLATION_GUIDE.md"
echo ""
echo "⚠️ Important: This bot is for educational purposes only."
echo "   Please ensure compliance with VFS Global's terms of service."

