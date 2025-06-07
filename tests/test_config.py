#!/usr/bin/env python3
"""
Tests for configuration module
"""

import pytest
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config


class TestScraperConfig:
    """Test scraper configuration"""
    
    def test_scraper_config_exists(self):
        """Test that SCRAPER_CONFIG exists and has required keys"""
        assert hasattr(config, 'SCRAPER_CONFIG')
        assert isinstance(config.SCRAPER_CONFIG, dict)
        
        required_keys = ['url', 'headless_mode', 'wait_timeout', 'page_load_delay']
        for key in required_keys:
            assert key in config.SCRAPER_CONFIG

    def test_scraper_config_values(self):
        """Test scraper configuration values"""
        scraper_config = config.SCRAPER_CONFIG
        
        # URL should be the Berlin service URL
        assert scraper_config['url'] == "https://service.berlin.de/dienstleistung/351180/"
        
        # Headless mode should be boolean
        assert isinstance(scraper_config['headless_mode'], bool)
        
        # Timeouts should be positive integers
        assert isinstance(scraper_config['wait_timeout'], int)
        assert scraper_config['wait_timeout'] > 0
        
        assert isinstance(scraper_config['page_load_delay'], int)
        assert scraper_config['page_load_delay'] > 0


class TestTextPatterns:
    """Test text patterns configuration"""
    
    def test_text_patterns_exists(self):
        """Test that TEXT_PATTERNS exists"""
        assert hasattr(config, 'TEXT_PATTERNS')
        assert isinstance(config.TEXT_PATTERNS, dict)

    def test_no_appointments_pattern(self):
        """Test no appointments text pattern"""
        patterns = config.TEXT_PATTERNS
        assert 'no_appointments' in patterns
        
        # Should contain the German text for no appointments
        no_appointments_text = patterns['no_appointments']
        assert isinstance(no_appointments_text, str)
        assert 'keine termine' in no_appointments_text.lower()


class TestSelectors:
    """Test CSS/ID selectors configuration"""
    
    def test_selectors_exists(self):
        """Test that SELECTORS exists"""
        assert hasattr(config, 'SELECTORS')
        assert isinstance(config.SELECTORS, dict)

    def test_required_selectors(self):
        """Test that required selectors are present"""
        selectors = config.SELECTORS
        
        required_selectors = ['checkbox_all_locations', 'submit_button']
        for selector in required_selectors:
            assert selector in selectors
            assert isinstance(selectors[selector], str)
            assert len(selectors[selector]) > 0

    def test_selector_values(self):
        """Test specific selector values"""
        selectors = config.SELECTORS
        
        # These are the actual IDs used on the Berlin website
        assert selectors['checkbox_all_locations'] == 'checkbox_overall'
        assert selectors['submit_button'] == 'appointment_submit'


class TestNotificationConfig:
    """Test notification configuration"""
    
    def test_notification_config_exists(self):
        """Test that NOTIFICATION_CONFIG exists"""
        assert hasattr(config, 'NOTIFICATION_CONFIG')
        assert isinstance(config.NOTIFICATION_CONFIG, dict)

    def test_notification_config_structure(self):
        """Test notification configuration structure"""
        notif_config = config.NOTIFICATION_CONFIG
        
        # Should have enabled flag
        assert 'enabled' in notif_config
        assert isinstance(notif_config['enabled'], bool)
        
        # Should have timeout
        assert 'timeout' in notif_config
        assert isinstance(notif_config['timeout'], int)
        assert notif_config['timeout'] > 0


class TestConfigIntegration:
    """Integration tests for configuration"""
    
    def test_all_configs_accessible(self):
        """Test that all main config objects are accessible"""
        configs = ['SCRAPER_CONFIG', 'TEXT_PATTERNS', 'SELECTORS', 'NOTIFICATION_CONFIG']
        
        for config_name in configs:
            assert hasattr(config, config_name)
            config_obj = getattr(config, config_name)
            assert isinstance(config_obj, dict)
            assert len(config_obj) > 0

    def test_config_consistency(self):
        """Test that configuration values are consistent"""
        # URL in SCRAPER_CONFIG should be a valid-looking URL
        url = config.SCRAPER_CONFIG['url']
        assert url.startswith('https://')
        assert 'berlin.de' in url
        
        # Selectors should be non-empty strings
        for selector_name, selector_value in config.SELECTORS.items():
            assert isinstance(selector_value, str)
            assert len(selector_value.strip()) > 0 