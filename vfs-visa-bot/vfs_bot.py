import time
import random
import logging
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    ElementClickInterceptedException,
    WebDriverException
)
import undetected_chromedriver as uc
from config import Config
from logger import log_error_with_screenshot, log_success_with_screenshot

class VFSBot:
    """Main VFS Global appointment booking bot"""
    
    def __init__(self, logger, notification_service):
        self.logger = logger
        self.notification_service = notification_service
        self.driver = None
        self.wait = None
        self.check_count = 0
        
    def setup_driver(self):
        """Setup undetected Chrome driver"""
        try:
            self.logger.info("Setting up Chrome driver...")
            
            # Chrome options
            options = uc.ChromeOptions()
            
            if Config.HEADLESS_MODE:
                options.add_argument('--headless')
            
            # Additional options to avoid detection
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Set user agent
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Create driver
            self.driver = uc.Chrome(options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Set timeouts
            self.driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
            self.driver.implicitly_wait(Config.IMPLICIT_WAIT)
            
            # Setup WebDriverWait
            self.wait = WebDriverWait(self.driver, Config.BROWSER_TIMEOUT)
            
            self.logger.info("Chrome driver setup completed successfully")
            return True
            
        except Exception as e:
            log_error_with_screenshot(self.logger, self.driver, "Failed to setup Chrome driver", e)
            return False
    
    def navigate_to_login(self):
        """Navigate to VFS Global login page"""
        try:
            login_url = f"{Config.VFS_BASE_URL}/login"
            self.logger.info(f"Navigating to login page: {login_url}")
            
            self.driver.get(login_url)
            
            # Wait for page to load
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # Add random delay to mimic human behavior
            time.sleep(random.uniform(2, 4))
            
            self.logger.info("Successfully navigated to login page")
            return True
            
        except Exception as e:
            log_error_with_screenshot(self.logger, self.driver, "Failed to navigate to login page", e)
            return False
    
    def login(self):
        """Login to VFS Global"""
        try:
            self.logger.info("Attempting to login...")
            
            # Find username field
            username_selectors = [
                "input[name='username']",
                "input[name='email']",
                "input[id='username']",
                "input[id='email']",
                "input[type='email']",
                "#mat-input-0",
                ".mat-input-element"
            ]
            
            username_field = None
            for selector in username_selectors:
                try:
                    username_field = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except TimeoutException:
                    continue
            
            if not username_field:
                raise Exception("Could not find username field")
            
            # Clear and enter username
            username_field.clear()
            time.sleep(random.uniform(0.5, 1))
            username_field.send_keys(Config.VFS_USERNAME)
            time.sleep(random.uniform(1, 2))
            
            # Find password field
            password_selectors = [
                "input[name='password']",
                "input[id='password']",
                "input[type='password']",
                "#mat-input-1"
            ]
            
            password_field = None
            for selector in password_selectors:
                try:
                    password_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if not password_field:
                raise Exception("Could not find password field")
            
            # Clear and enter password
            password_field.clear()
            time.sleep(random.uniform(0.5, 1))
            password_field.send_keys(Config.VFS_PASSWORD)
            time.sleep(random.uniform(1, 2))
            
            # Find and click login button
            login_button_selectors = [
                "button[type='submit']",
                "input[type='submit']",
                "button:contains('Login')",
                "button:contains('Sign In')",
                ".login-button",
                ".btn-login",
                "#login-button"
            ]
            
            login_button = None
            for selector in login_button_selectors:
                try:
                    login_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if not login_button:
                # Try to find button by text
                try:
                    login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'Sign In') or contains(text(), 'Giriş')]")
                except NoSuchElementException:
                    raise Exception("Could not find login button")
            
            # Click login button
            self.driver.execute_script("arguments[0].click();", login_button)
            time.sleep(random.uniform(2, 4))
            
            # Wait for login to complete (check for dashboard or appointment page)
            try:
                # Wait for either successful login redirect or error message
                self.wait.until(
                    lambda driver: (
                        "dashboard" in driver.current_url.lower() or
                        "appointment" in driver.current_url.lower() or
                        "randevu" in driver.current_url.lower() or
                        driver.find_elements(By.CSS_SELECTOR, ".error, .alert-danger, .mat-error")
                    )
                )
                
                # Check if there are any error messages
                error_elements = self.driver.find_elements(By.CSS_SELECTOR, ".error, .alert-danger, .mat-error")
                if error_elements:
                    error_text = error_elements[0].text
                    raise Exception(f"Login failed: {error_text}")
                
                self.logger.info("Login successful")
                return True
                
            except TimeoutException:
                # Check if we're still on login page
                if "login" in self.driver.current_url.lower():
                    raise Exception("Login failed - still on login page")
                else:
                    self.logger.info("Login appears successful")
                    return True
            
        except Exception as e:
            log_error_with_screenshot(self.logger, self.driver, "Login failed", e)
            return False
    
    def navigate_to_appointments(self):
        """Navigate to appointments page"""
        try:
            self.logger.info("Navigating to appointments page...")
            
            # Common appointment page URLs and selectors
            appointment_urls = [
                f"{Config.VFS_BASE_URL}/book-your-appointment",
                f"{Config.VFS_BASE_URL}/appointment",
                f"{Config.VFS_BASE_URL}/randevu"
            ]
            
            appointment_selectors = [
                "a[href*='appointment']",
                "a[href*='randevu']",
                "a:contains('Book Appointment')",
                "a:contains('Randevu Al')",
                ".appointment-link",
                ".book-appointment"
            ]
            
            # First try to find appointment link on current page
            for selector in appointment_selectors:
                try:
                    appointment_link = self.driver.find_element(By.CSS_SELECTOR, selector)
                    self.driver.execute_script("arguments[0].click();", appointment_link)
                    time.sleep(random.uniform(2, 4))
                    self.logger.info("Found and clicked appointment link")
                    return True
                except NoSuchElementException:
                    continue
            
            # If no link found, try direct URLs
            for url in appointment_urls:
                try:
                    self.driver.get(url)
                    time.sleep(random.uniform(2, 4))
                    
                    # Check if page loaded successfully
                    if "appointment" in self.driver.current_url.lower() or "randevu" in self.driver.current_url.lower():
                        self.logger.info(f"Successfully navigated to: {url}")
                        return True
                        
                except Exception:
                    continue
            
            raise Exception("Could not navigate to appointments page")
            
        except Exception as e:
            log_error_with_screenshot(self.logger, self.driver, "Failed to navigate to appointments page", e)
            return False
    
    def check_available_appointments(self):
        """Check for available appointments"""
        try:
            self.logger.info("Checking for available appointments...")
            self.check_count += 1
            
            # Refresh the page to get latest data
            self.driver.refresh()
            time.sleep(random.uniform(3, 5))
            
            # Look for appointment calendar or available slots
            appointment_selectors = [
                ".available-slot",
                ".appointment-slot",
                ".calendar-day.available",
                ".date-available",
                "button:not([disabled])[data-date]",
                ".fc-day:not(.fc-disabled)",
                ".available-time"
            ]
            
            available_appointments = []
            
            for selector in appointment_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        self.logger.info(f"Found {len(elements)} potential appointment slots with selector: {selector}")
                        
                        for element in elements:
                            try:
                                # Extract date and time information
                                date_text = element.get_attribute('data-date') or element.text
                                if date_text and date_text.strip():
                                    available_appointments.append({
                                        'element': element,
                                        'date': date_text,
                                        'selector': selector
                                    })
                            except Exception:
                                continue
                        
                        if available_appointments:
                            break
                            
                except Exception:
                    continue
            
            if available_appointments:
                self.logger.info(f"Found {len(available_appointments)} available appointments")
                return available_appointments
            else:
                self.logger.info("No available appointments found")
                self.notification_service.send_no_appointment_notification(self.check_count)
                return []
            
        except Exception as e:
            log_error_with_screenshot(self.logger, self.driver, "Failed to check appointments", e)
            return []
    
    def book_appointment(self, appointment):
        """Book the selected appointment"""
        try:
            self.logger.info(f"Attempting to book appointment: {appointment['date']}")
            
            # Click on the appointment slot
            element = appointment['element']
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(random.uniform(1, 2))
            
            self.driver.execute_script("arguments[0].click();", element)
            time.sleep(random.uniform(2, 4))
            
            # Look for confirmation button
            confirm_selectors = [
                "button:contains('Confirm')",
                "button:contains('Book')",
                "button:contains('Onayla')",
                "button:contains('Randevu Al')",
                ".confirm-button",
                ".book-button",
                "input[type='submit'][value*='confirm']"
            ]
            
            for selector in confirm_selectors:
                try:
                    confirm_button = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    self.driver.execute_script("arguments[0].click();", confirm_button)
                    time.sleep(random.uniform(2, 4))
                    break
                except TimeoutException:
                    continue
            
            # Check for success message or confirmation
            success_selectors = [
                ".success-message",
                ".confirmation",
                ".alert-success",
                ".booking-confirmed"
            ]
            
            success_found = False
            for selector in success_selectors:
                try:
                    success_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if success_element.is_displayed():
                        success_found = True
                        break
                except NoSuchElementException:
                    continue
            
            if success_found or "confirmation" in self.driver.current_url.lower():
                appointment_details = {
                    'date': appointment['date'],
                    'time': appointment.get('time', 'N/A'),
                    'center': Config.APPLICATION_CENTER,
                    'visa_type': Config.VISA_TYPE
                }
                
                log_success_with_screenshot(self.logger, self.driver, f"Appointment booked successfully: {appointment_details}")
                self.notification_service.send_success_notification(appointment_details)
                return True
            else:
                raise Exception("Could not confirm appointment booking")
            
        except Exception as e:
            log_error_with_screenshot(self.logger, self.driver, "Failed to book appointment", e)
            return False
    
    def run_single_check(self):
        """Run a single appointment check cycle"""
        try:
            if not self.driver:
                if not self.setup_driver():
                    return False
                
                if not self.navigate_to_login():
                    return False
                
                if not self.login():
                    return False
                
                if not self.navigate_to_appointments():
                    return False
            
            # Check for available appointments
            available_appointments = self.check_available_appointments()
            
            if available_appointments:
                # Try to book the first available appointment
                for appointment in available_appointments:
                    if self.book_appointment(appointment):
                        return True  # Successfully booked
                    else:
                        # If booking failed, try next appointment
                        continue
            
            return False  # No appointments booked
            
        except Exception as e:
            log_error_with_screenshot(self.logger, self.driver, "Error during appointment check", e)
            return False
    
    def run(self):
        """Main bot execution loop"""
        try:
            self.logger.info("Starting VFS appointment bot...")
            self.notification_service.send_start_notification()
            
            while True:
                try:
                    self.logger.info(f"Starting check cycle #{self.check_count + 1}")
                    
                    if self.run_single_check():
                        self.logger.info("Appointment successfully booked! Stopping bot.")
                        break
                    
                    self.logger.info(f"No appointments booked. Waiting {Config.CHECK_INTERVAL} seconds before next check...")
                    time.sleep(Config.CHECK_INTERVAL)
                    
                except KeyboardInterrupt:
                    self.logger.info("Bot stopped by user")
                    break
                    
                except Exception as e:
                    log_error_with_screenshot(self.logger, self.driver, "Error in main loop", e)
                    self.notification_service.send_error_notification(str(e))
                    
                    # Wait before retrying
                    time.sleep(Config.RETRY_DELAY)
                    
                    # Reset driver if needed
                    try:
                        if self.driver:
                            self.driver.quit()
                    except:
                        pass
                    self.driver = None
            
        except Exception as e:
            log_error_with_screenshot(self.logger, self.driver, "Critical error in bot execution", e)
            self.notification_service.send_error_notification(f"Critical error: {str(e)}")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            if self.driver:
                self.logger.info("Closing browser...")
                self.driver.quit()
                self.driver = None
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")
        
        self.logger.info("Bot execution completed")

