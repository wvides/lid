#!/usr/bin/env python3
"""
Tests for Berlin Appointment Scraper
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the parent directory to the path to import the scraper
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from berlin_appointment_scraper import BerlinAppointmentScraper


class TestBerlinAppointmentScraper:
    """Test cases for the BerlinAppointmentScraper class"""

    def test_init_headless_true(self):
        """Test scraper initialization with headless=True"""
        scraper = BerlinAppointmentScraper(headless=True)
        assert scraper.headless is True
        assert scraper.url == "https://service.berlin.de/dienstleistung/351180/"
        assert scraper.driver is None

    def test_init_headless_false(self):
        """Test scraper initialization with headless=False"""
        scraper = BerlinAppointmentScraper(headless=False)
        assert scraper.headless is False
        assert scraper.url == "https://service.berlin.de/dienstleistung/351180/"

    @patch('berlin_appointment_scraper.webdriver.Chrome')
    @patch('berlin_appointment_scraper.ChromeDriverManager')
    def test_setup_driver_success(self, mock_driver_manager, mock_chrome):
        """Test successful driver setup"""
        # Mock ChromeDriverManager
        mock_driver_manager.return_value.install.return_value = "/path/to/chromedriver"
        
        # Mock Chrome webdriver
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        
        scraper = BerlinAppointmentScraper(headless=True)
        scraper.setup_driver()
        
        assert scraper.driver == mock_driver
        mock_chrome.assert_called_once()

    @patch('berlin_appointment_scraper.webdriver.Chrome')
    @patch('berlin_appointment_scraper.ChromeDriverManager')
    def test_setup_driver_fallback(self, mock_driver_manager, mock_chrome):
        """Test driver setup with fallback when ChromeDriverManager fails"""
        # Mock ChromeDriverManager to raise exception
        mock_driver_manager.return_value.install.side_effect = Exception("Download failed")
        
        # Mock Chrome webdriver for fallback
        mock_driver = MagicMock()
        mock_chrome_calls = [Mock(side_effect=Exception("First call fails")), mock_driver]
        mock_chrome.side_effect = mock_chrome_calls
        
        scraper = BerlinAppointmentScraper(headless=True)
        
        # This should not raise an exception and should use fallback
        with patch('builtins.print'):  # Suppress print output
            scraper.setup_driver()

    def test_send_notification(self):
        """Test notification sending (currently just prints)"""
        scraper = BerlinAppointmentScraper()
        
        # Capture print output
        with patch('builtins.print') as mock_print:
            scraper.send_notification("Test message")
            mock_print.assert_called_with("🔔 NOTIFICATION: Test message")

    @patch.object(BerlinAppointmentScraper, 'setup_driver')
    def test_check_appointments_driver_setup_called(self, mock_setup_driver):
        """Test that check_appointments calls setup_driver"""
        scraper = BerlinAppointmentScraper()
        mock_driver = MagicMock()
        scraper.driver = mock_driver
        
        # Mock driver methods to avoid actual web requests
        mock_driver.get.return_value = None
        mock_driver.page_source = "Leider sind aktuell keine Termine für ihre Auswahl verfügbar."
        
        with patch('berlin_appointment_scraper.WebDriverWait'):
            scraper.check_appointments()
            
        mock_setup_driver.assert_called_once()

    def test_check_appointments_no_appointments(self):
        """Test check_appointments when no appointments are available"""
        scraper = BerlinAppointmentScraper()
        mock_driver = MagicMock()
        
        # Mock the driver and its methods
        mock_driver.page_source = "Leider sind aktuell keine Termine für ihre Auswahl verfügbar."
        mock_driver.get.return_value = None
        
        # Mock WebDriverWait and elements
        with patch('berlin_appointment_scraper.WebDriverWait') as mock_wait:
            mock_element = MagicMock()
            mock_element.is_selected.return_value = False
            mock_wait.return_value.until.return_value = mock_element
            
            with patch.object(scraper, 'setup_driver'):
                scraper.driver = mock_driver
                result = scraper.check_appointments()
                
        assert result is False

    def test_check_appointments_appointments_available(self):
        """Test check_appointments when appointments might be available"""
        scraper = BerlinAppointmentScraper()
        mock_driver = MagicMock()
        
        # Mock the driver with page source that doesn't contain "no appointments" message
        mock_driver.page_source = "Some other content without the no appointments message"
        mock_driver.current_url = "https://service.berlin.de/appointment-page"
        mock_driver.get.return_value = None
        
        # Mock WebDriverWait and elements
        with patch('berlin_appointment_scraper.WebDriverWait') as mock_wait:
            mock_element = MagicMock()
            mock_element.is_selected.return_value = False
            mock_wait.return_value.until.return_value = mock_element
            
            with patch.object(scraper, 'setup_driver'):
                with patch.object(scraper, 'send_notification') as mock_notify:
                    scraper.driver = mock_driver
                    result = scraper.check_appointments()
                    
                    mock_notify.assert_called_once()
                    
        assert result is True

    def test_check_appointments_timeout_exception(self):
        """Test check_appointments handles TimeoutException"""
        from selenium.common.exceptions import TimeoutException
        
        scraper = BerlinAppointmentScraper()
        
        with patch.object(scraper, 'setup_driver'):
            with patch('berlin_appointment_scraper.WebDriverWait') as mock_wait:
                mock_wait.return_value.until.side_effect = TimeoutException()
                
                with patch('builtins.print'):  # Suppress print output
                    result = scraper.check_appointments()
                    
        assert result is False

    def test_check_appointments_no_such_element_exception(self):
        """Test check_appointments handles NoSuchElementException"""
        from selenium.common.exceptions import NoSuchElementException
        
        scraper = BerlinAppointmentScraper()
        
        with patch.object(scraper, 'setup_driver'):
            with patch('berlin_appointment_scraper.WebDriverWait') as mock_wait:
                mock_wait.return_value.until.side_effect = NoSuchElementException()
                
                with patch('builtins.print'):  # Suppress print output
                    result = scraper.check_appointments()
                    
        assert result is False

    def test_check_appointments_general_exception(self):
        """Test check_appointments handles general exceptions"""
        scraper = BerlinAppointmentScraper()
        
        with patch.object(scraper, 'setup_driver', side_effect=Exception("General error")):
            with patch('builtins.print'):  # Suppress print output
                result = scraper.check_appointments()
                
        assert result is False

    def test_check_appointments_driver_cleanup(self):
        """Test that driver is properly cleaned up after check_appointments"""
        scraper = BerlinAppointmentScraper()
        mock_driver = MagicMock()
        
        with patch.object(scraper, 'setup_driver'):
            scraper.driver = mock_driver
            
            # Force an exception to test cleanup
            mock_driver.get.side_effect = Exception("Test exception")
            
            with patch('builtins.print'):  # Suppress print output
                scraper.check_appointments()
                
            # Verify driver.quit() was called
            mock_driver.quit.assert_called_once()

    def test_run_check_success(self):
        """Test run_check method returns check_appointments result"""
        scraper = BerlinAppointmentScraper()
        
        with patch.object(scraper, 'check_appointments', return_value=True):
            result = scraper.run_check()
            
        assert result is True

    def test_run_check_exception_handling(self):
        """Test run_check handles exceptions from check_appointments"""
        scraper = BerlinAppointmentScraper()
        
        with patch.object(scraper, 'check_appointments', side_effect=Exception("Test error")):
            with patch('builtins.print'):  # Suppress print output
                result = scraper.run_check()
                
        assert result is False


class TestScraperIntegration:
    """Integration tests for the scraper"""
    
    def test_main_function_exists(self):
        """Test that main function exists and can be imported"""
        from berlin_appointment_scraper import main
        assert callable(main)

    @patch('berlin_appointment_scraper.BerlinAppointmentScraper')
    def test_main_function_execution(self, mock_scraper_class):
        """Test main function creates scraper and runs check"""
        mock_scraper = MagicMock()
        mock_scraper.run_check.return_value = False
        mock_scraper_class.return_value = mock_scraper
        
        from berlin_appointment_scraper import main
        
        with patch('builtins.print'):  # Suppress print output
            main()
            
        mock_scraper_class.assert_called_once()
        mock_scraper.run_check.assert_called_once()


class TestConfiguration:
    """Test configuration and constants"""
    
    def test_scraper_url(self):
        """Test that scraper has correct URL"""
        scraper = BerlinAppointmentScraper()
        expected_url = "https://service.berlin.de/dienstleistung/351180/"
        assert scraper.url == expected_url

    def test_headless_default(self):
        """Test default headless setting"""
        scraper = BerlinAppointmentScraper()
        # Default should be True based on constructor
        assert scraper.headless is True 