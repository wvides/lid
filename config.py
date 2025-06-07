#!/usr/bin/env python3
"""
Configuration file for Berlin Appointment Scraper
"""

# Scraper settings
SCRAPER_CONFIG = {
    "url": "https://service.berlin.de/dienstleistung/351180/",
    "headless_mode": True,  # Set to False to see the browser in action
    "wait_timeout": 10,  # seconds to wait for elements
    "page_load_delay": 3,  # seconds to wait after clicking submit
}

# Text patterns to check for
TEXT_PATTERNS = {
    "no_appointments": "Leider sind aktuell keine Termine für ihre Auswahl verfügbar.",
    # Add more patterns if needed
}

# Element selectors
SELECTORS = {
    "checkbox_all_locations": "checkbox_overall",
    "submit_button": "appointment_submit",
}

# Notification settings
NOTIFICATION_CONFIG = {
    "enabled": True,
    # "endpoint_url": "YOUR_NOTIFICATION_ENDPOINT_HERE",  # Uncomment and set your URL
    "timeout": 10,  # seconds
} 