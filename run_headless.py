#!/usr/bin/env python3
"""
Headless Berlin Appointment Scraper for Server Deployment
Optimized for running on remote servers without display
"""

import sys
import logging
from datetime import datetime
from berlin_appointment_scraper import BerlinAppointmentScraper


def setup_logging():
    """Setup logging for server deployment"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('appointment_scraper.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


def main():
    """Main function for headless server deployment"""
    logger = setup_logging()
    
    logger.info("=" * 60)
    logger.info("🇩🇪 Berlin Appointment Scraper - Headless Mode")
    logger.info(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    try:
        # Force headless mode for server deployment
        scraper = BerlinAppointmentScraper(headless=True)
        
        logger.info("🚀 Starting appointment check in headless mode...")
        result = scraper.run_check()
        
        if result:
            logger.warning("🎉 APPOINTMENTS FOUND! Check your notifications!")
        else:
            logger.info("💤 No appointments available")
            
    except Exception as e:
        logger.error(f"❌ Critical error: {e}")
        sys.exit(1)
    
    logger.info(f"✅ Check completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main() 