#!/usr/bin/env python3
"""
VFS Global Appointment Bot
Automatically checks and books visa appointments on VFS Global website
"""

import sys
import signal
from config import Config
from logger import setup_logger
from notification import NotificationService
from vfs_bot import VFSBot

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\nBot stopped by user")
    sys.exit(0)

def main():
    """Main entry point"""
    try:
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)
        
        # Validate configuration
        Config.validate()
        
        # Setup logging
        logger = setup_logger()
        logger.info("VFS Global Appointment Bot starting...")
        
        # Initialize notification service
        notification_service = NotificationService()
        
        # Initialize and run bot
        bot = VFSBot(logger, notification_service)
        bot.run()
        
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please check your .env file and ensure all required fields are set.")
        sys.exit(1)
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

