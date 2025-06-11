#!/usr/bin/env python3
"""
VFS Global Appointment Bot - Test Script
Tests basic functionality without actual VFS Global connection
"""

import sys
import os
import logging
from unittest.mock import Mock, patch

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    try:
        from config import Config
        from logger import setup_logger
        from notification import NotificationService
        from vfs_bot import VFSBot
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration loading"""
    try:
        from config import Config
        
        # Test with default values
        print(f"✅ Config loaded - Base URL: {Config.VFS_BASE_URL}")
        print(f"✅ Config loaded - Check Interval: {Config.CHECK_INTERVAL}")
        print(f"✅ Config loaded - Headless Mode: {Config.HEADLESS_MODE}")
        
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_logger():
    """Test logger setup"""
    try:
        from logger import setup_logger
        
        logger = setup_logger()
        logger.info("Test log message")
        print("✅ Logger setup successful")
        return True
    except Exception as e:
        print(f"❌ Logger error: {e}")
        return False

def test_notification():
    """Test notification service"""
    try:
        from notification import NotificationService
        
        notification_service = NotificationService()
        print("✅ Notification service initialized")
        
        # Test with disabled notifications (should not fail)
        result = notification_service.send_telegram_message("Test message")
        print(f"✅ Telegram test completed (disabled): {result}")
        
        return True
    except Exception as e:
        print(f"❌ Notification error: {e}")
        return False

def test_bot_initialization():
    """Test bot initialization without browser"""
    try:
        from vfs_bot import VFSBot
        from logger import setup_logger
        from notification import NotificationService
        
        logger = setup_logger()
        notification_service = NotificationService()
        
        bot = VFSBot(logger, notification_service)
        print("✅ Bot initialized successfully")
        
        return True
    except Exception as e:
        print(f"❌ Bot initialization error: {e}")
        return False

def test_selenium_import():
    """Test Selenium and undetected-chromedriver imports"""
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import undetected_chromedriver as uc
        
        print("✅ Selenium and undetected-chromedriver imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Selenium import error: {e}")
        return False

def test_chrome_availability():
    """Test if Chrome is available"""
    try:
        import subprocess
        
        # Try to get Chrome version
        try:
            result = subprocess.run(['google-chrome', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"✅ Google Chrome found: {result.stdout.strip()}")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Try alternative Chrome commands
        chrome_commands = [
            'chromium-browser',
            'chromium',
            '/usr/bin/google-chrome',
            '/usr/bin/chromium-browser'
        ]
        
        for cmd in chrome_commands:
            try:
                result = subprocess.run([cmd, '--version'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"✅ Chrome found: {result.stdout.strip()}")
                    return True
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        print("⚠️ Chrome not found - bot will try to download ChromeDriver automatically")
        return True  # Not a critical error, undetected-chromedriver can handle this
        
    except Exception as e:
        print(f"⚠️ Chrome check error: {e}")
        return True  # Not critical

def run_all_tests():
    """Run all tests"""
    print("🧪 VFS Global Appointment Bot - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_config),
        ("Logger", test_logger),
        ("Notification Service", test_notification),
        ("Bot Initialization", test_bot_initialization),
        ("Selenium Imports", test_selenium_import),
        ("Chrome Availability", test_chrome_availability),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Bot is ready to use.")
        print("\n📝 Next steps:")
        print("1. Edit .env file with your VFS Global credentials")
        print("2. Run: python main.py")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

