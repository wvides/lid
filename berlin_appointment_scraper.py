#!/usr/bin/env python3
"""
Berlin Appointment Scraper
Checks for available appointments for the Einbürgerungstest (citizenship test)
"""

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


class BerlinAppointmentScraper:
    def __init__(self, headless=True):
        """Initialize the scraper with Chrome options"""
        self.url = "https://service.berlin.de/dienstleistung/351180/"
        self.driver = None
        self.headless = headless
        
    def setup_driver(self):
        """Setup Chrome driver with appropriate options"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Additional options for server/headless environments
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--remote-debugging-port=9222")
        
        # Set Chrome binary path for different systems
        import platform
        system = platform.system()
        if system == "Darwin":  # macOS
            chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        elif system == "Linux":  # Linux servers
            # Common Chrome paths on Linux
            chrome_paths = [
                "/usr/bin/google-chrome",
                "/usr/bin/google-chrome-stable",
                "/usr/bin/chromium-browser",
                "/usr/bin/chromium"
            ]
            import os
            for path in chrome_paths:
                if os.path.exists(path):
                    chrome_options.binary_location = path
                    break
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            print(f"❌ Error setting up ChromeDriver: {e}")
            print("🔧 Trying alternative ChromeDriver setup...")
            # Try without webdriver manager
            self.driver = webdriver.Chrome(options=chrome_options)
        
    def send_notification(self, message):
        """
        Send notification when appointments are available
        TODO: Replace with your notification endpoint URL
        """
        # NOTIFICATION ENDPOINT - Replace with your actual endpoint
        # notification_url = "YOUR_NOTIFICATION_ENDPOINT_HERE"
        
        # payload = {
        #     "message": message,
        #     "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        #     "source": "Berlin Appointment Scraper"
        # }
        
        # try:
        #     response = requests.post(notification_url, json=payload, timeout=10)
        #     if response.status_code == 200:
        #         print(f"✅ Notification sent successfully: {message}")
        #     else:
        #         print(f"❌ Failed to send notification. Status code: {response.status_code}")
        # except requests.RequestException as e:
        #     print(f"❌ Error sending notification: {e}")
        
        # For now, just print the message
        print(f"🔔 NOTIFICATION: {message}")
        
    def check_appointments(self):
        """
        Main function to check for available appointments
        Returns True if appointments are available, False otherwise
        """
        try:
            print("🚀 Starting Berlin appointment check...")
            
            # Setup driver
            self.setup_driver()
            
            # Navigate to the page
            print(f"📱 Navigating to: {self.url}")
            self.driver.get(self.url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Find and click the "Alle Standorte auswählen" checkbox
            print("🔍 Looking for 'Alle Standorte auswählen' checkbox...")
            
            checkbox = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "checkbox_overall"))
            )
            
            if not checkbox.is_selected():
                print("✅ Selecting 'Alle Standorte auswählen' checkbox...")
                # Scroll to the element to ensure it's visible
                self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                time.sleep(0.5)  # Small delay after scrolling
                
                # Try JavaScript click to avoid overlay issues
                try:
                    self.driver.execute_script("arguments[0].click();", checkbox)
                except Exception as e:
                    print(f"⚠️ JavaScript click failed, trying regular click: {e}")
                    checkbox.click()
                
                time.sleep(1)  # Small delay to ensure the checkbox is selected
            else:
                print("ℹ️ Checkbox already selected")
            
            # Find and click the submit button
            print("🔍 Looking for submit button...")
            
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "appointment_submit"))
            )
            
            print("🔄 Clicking submit button...")
            submit_button.click()
            
            # Wait for the new page to load
            print("⏳ Waiting for results page to load...")
            time.sleep(3)  # Give the page time to load
            
            # Check for the "no appointments available" message
            no_appointments_text = "Leider sind aktuell keine Termine für ihre Auswahl verfügbar."
            
            page_source = self.driver.page_source.lower()
            no_appointments_found = no_appointments_text.lower() in page_source
            
            if no_appointments_found:
                print("❌ No appointments available")
                return False
            else:
                print("🎉 APPOINTMENTS MIGHT BE AVAILABLE!")
                current_url = self.driver.current_url
                message = f"Appointments might be available! Check: {current_url}"
                self.send_notification(message)
                return True
                
        except TimeoutException:
            print("⏰ Timeout waiting for page elements")
            return False
        except NoSuchElementException as e:
            print(f"❌ Element not found: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                print("🔒 Browser closed")
    
    def run_check(self):
        """Public method to run the appointment check"""
        try:
            return self.check_appointments()
        except Exception as e:
            print(f"❌ Error during appointment check: {e}")
            return False


def main():
    """Main function to run the scraper"""
    print("=" * 50)
    print("🇩🇪 Berlin Appointment Scraper")
    print("=" * 50)
    
    scraper = BerlinAppointmentScraper(headless=False)  # Visible browser for basic mode
    
    result = scraper.run_check()
    
    if result:
        print("\n✨ Check completed - Appointments found!")
    else:
        print("\n💤 Check completed - No appointments available")
    
    print("=" * 50)


if __name__ == "__main__":
    main() 