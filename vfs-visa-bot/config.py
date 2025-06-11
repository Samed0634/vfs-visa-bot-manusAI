import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for VFS Visa Bot"""
    
    # VFS Global Credentials
    VFS_USERNAME = os.getenv('VFS_USERNAME')
    VFS_PASSWORD = os.getenv('VFS_PASSWORD')
    
    # VFS Global Configuration
    VFS_BASE_URL = os.getenv('VFS_BASE_URL', 'https://visa.vfsglobal.com/tur/tr/nld')
    VISA_TYPE = os.getenv('VISA_TYPE', 'Tourism')
    APPLICATION_CENTER = os.getenv('APPLICATION_CENTER', 'Ankara')
    PREFERRED_DATE_START = os.getenv('PREFERRED_DATE_START', '2025-07-01')
    PREFERRED_DATE_END = os.getenv('PREFERRED_DATE_END', '2025-12-31')
    PREFERRED_TIME_START = os.getenv('PREFERRED_TIME_START', '09:00')
    PREFERRED_TIME_END = os.getenv('PREFERRED_TIME_END', '17:00')
    
    # Bot Configuration
    CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 300))  # 5 minutes
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY', 10))
    HEADLESS_MODE = os.getenv('HEADLESS_MODE', 'false').lower() == 'true'
    SCREENSHOT_ON_ERROR = os.getenv('SCREENSHOT_ON_ERROR', 'true').lower() == 'true'
    
    # Notification Configuration
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    ENABLE_NOTIFICATIONS = os.getenv('ENABLE_NOTIFICATIONS', 'false').lower() == 'true'
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'vfs_bot.log')
    
    # Browser Configuration
    BROWSER_TIMEOUT = int(os.getenv('BROWSER_TIMEOUT', 30))
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', 30))
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', 10))
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required_fields = ['VFS_USERNAME', 'VFS_PASSWORD']
        missing_fields = []
        
        for field in required_fields:
            if not getattr(cls, field):
                missing_fields.append(field)
        
        if missing_fields:
            raise ValueError(f"Missing required configuration: {', '.join(missing_fields)}")
        
        return True
    
    @classmethod
    def get_log_level(cls):
        """Get logging level from string"""
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        return level_map.get(cls.LOG_LEVEL.upper(), logging.INFO)

