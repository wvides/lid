#!/usr/bin/env python3
"""
Test script for Berlin Appointment Scraper
"""

from berlin_appointment_scraper import BerlinAppointmentScraper


def test_scraper():
    """Test the scraper with visible browser for debugging"""
    print("🧪 Testing Berlin Appointment Scraper")
    print("-" * 40)
    
    # Create scraper instance with visible browser for testing
    scraper = BerlinAppointmentScraper(headless=False)
    
    # Run the check
    result = scraper.run_check()
    
    print(f"\n📊 Test Result: {'✅ Success' if result is not None else '❌ Failed'}")
    print(f"🎯 Appointments Available: {'Yes' if result else 'No'}")
    
    return result


if __name__ == "__main__":
    test_scraper() 