import logging
import os
from datetime import datetime
from config import Config

def setup_logger():
    """Setup logging configuration"""
    
    # Create logs directory if it doesn't exist
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create log filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = f"{log_dir}/vfs_bot_{timestamp}.log"
    
    # Configure logging
    logging.basicConfig(
        level=Config.get_log_level(),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    logger = logging.getLogger('VFS_Bot')
    logger.info(f"Logging initialized. Log file: {log_filename}")
    
    return logger

def log_error_with_screenshot(logger, driver, error_msg, exception=None):
    """Log error with screenshot if enabled"""
    logger.error(error_msg)
    
    if exception:
        logger.error(f"Exception details: {str(exception)}")
    
    if Config.SCREENSHOT_ON_ERROR and driver:
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_dir = 'screenshots'
            
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            
            screenshot_path = f"{screenshot_dir}/error_{timestamp}.png"
            driver.save_screenshot(screenshot_path)
            logger.info(f"Error screenshot saved: {screenshot_path}")
            
            # Also save page source
            page_source_path = f"{screenshot_dir}/error_{timestamp}.html"
            with open(page_source_path, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            logger.info(f"Page source saved: {page_source_path}")
            
        except Exception as e:
            logger.error(f"Failed to save error screenshot: {str(e)}")

def log_success_with_screenshot(logger, driver, success_msg):
    """Log success with screenshot"""
    logger.info(success_msg)
    
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_dir = 'screenshots'
        
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        
        screenshot_path = f"{screenshot_dir}/success_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        logger.info(f"Success screenshot saved: {screenshot_path}")
        
    except Exception as e:
        logger.error(f"Failed to save success screenshot: {str(e)}")

