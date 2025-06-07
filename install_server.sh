#!/bin/bash
# Server Installation Script for Berlin Appointment Scraper
# This script installs Chrome and Python dependencies on Ubuntu/Debian servers

echo "🇩🇪 Berlin Appointment Scraper - Server Installation"
echo "=================================================="

# Update package list
echo "📦 Updating package list..."
sudo apt-get update

# Install Python 3 and pip if not already installed
echo "🐍 Installing Python 3 and pip..."
sudo apt-get install -y python3 python3-pip

# Install Chrome dependencies
echo "🌐 Installing Chrome dependencies..."
sudo apt-get install -y wget gnupg

# Add Google Chrome repository
echo "📥 Adding Google Chrome repository..."
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list

# Update package list with new repository
sudo apt-get update

# Install Google Chrome
echo "🌐 Installing Google Chrome..."
sudo apt-get install -y google-chrome-stable

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip3 install -r requirements.txt

# Make scripts executable
chmod +x run_headless.py
chmod +x berlin_appointment_scraper.py

echo "✅ Installation completed!"
echo ""
echo "🚀 To run the scraper in headless mode:"
echo "   python3 run_headless.py"
echo ""
echo "📅 To set up a cron job (every 30 minutes):"
echo "   crontab -e"
echo "   Add this line:"
echo "   */30 * * * * cd $(pwd) && python3 run_headless.py"
echo ""
echo "📋 Check logs in: appointment_scraper.log" 