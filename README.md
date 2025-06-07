# Berlin Appointment Scraper 🇩🇪

A Python web scraper that automatically checks for available appointments for the Einbürgerungstest (German citizenship test) on the Berlin service portal.

## Features

- ✅ Automatically selects "Alle Standorte auswählen" (All locations)
- 🔄 Submits the appointment request form
- 🔍 Checks for appointment availability
- 🔔 Notification system ready for integration
- 🎛️ Configurable settings
- 🚀 Ready for scheduling/automation
- 🖥️ **Headless mode for remote servers**
- 📊 **Comprehensive logging**

## Prerequisites

- Python 3.7 or higher (⚠️ **Note**: Python 3.13 has compatibility issues with lxml - see Installation section)
- Chrome browser installed
- Internet connection
- Make (for using the Makefile - optional but recommended)

## Virtual Environment Setup (Recommended)

It's recommended to use a virtual environment to avoid conflicts with other Python projects:

### **Option 1: Using venv (Built-in)**

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Your terminal prompt should now show (venv)
```

### **Option 2: Using virtualenv**

```bash
# Install virtualenv if not already installed
pip3 install virtualenv

# Create virtual environment
virtualenv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### **Deactivating Virtual Environment**

When you're done working with the project:

```bash
deactivate
```

**Note:** Remember to activate your virtual environment every time you work with this project!

## Installation

1. **Clone or download this repository**

2. **Activate your virtual environment** (if you set one up):
   ```bash
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```
   
   **⚠️ Python 3.13 Compatibility Note:**
   If you encounter issues with `lxml` installation on Python 3.13, the scraper will work without it. The `lxml` dependency has been commented out in `requirements.txt` for compatibility.

4. **The script will automatically download ChromeDriver** using webdriver-manager

5. **Verify installation by running tests** (optional but recommended):
   ```bash
   make test
   # or
   python3 -m pytest tests/ -v
   ```

## Usage

### **🚀 Using the Makefile (Recommended)**

The project includes a comprehensive Makefile for easy management:

```bash
# See all available commands
make help

# Quick setup (create venv + install dependencies + dev tools)
make dev-setup

# Run the scraper in different modes
make run-test      # Visible browser mode
make run-headless  # Headless mode (recommended)
make run-basic     # Basic mode

# Testing and development
make test          # Run all tests
make test-watch    # Run tests in watch mode
make lint          # Check code quality
make format        # Format code

# Maintenance
make logs          # View recent logs
make logs-tail     # Tail logs in real-time
make clean         # Clean up temporary files
make check-deps    # Check for dependency issues

# Automation
make cron-setup    # Setup automated cron job
make cron-stop     # Remove cron job
```

### **Manual Usage**

If you prefer not to use the Makefile:

#### Basic Usage (Local)

```bash
python3 berlin_appointment_scraper.py
```

#### Test Mode (with visible browser)

```bash
python3 test_scraper.py
```

#### **🚀 Headless Mode (for servers) - RECOMMENDED**

```bash
python3 run_headless.py
```

## Server Deployment 🚀

### **Quick Server Setup (Ubuntu/Debian)**

1. **Upload files to your server:**
   ```bash
   scp -r * user@your-server:/path/to/scraper/
   ```

2. **Run the installation script:**
   ```bash
   chmod +x install_server.sh
   ./install_server.sh
   ```

3. **Run in headless mode:**
   ```bash
   python3 run_headless.py
   ```

### **Manual Server Setup**

1. **Install Chrome on Linux server:**
   ```bash
   # Ubuntu/Debian
   wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
   echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
   sudo apt-get update
   sudo apt-get install -y google-chrome-stable
   
   # CentOS/RHEL
   sudo yum install -y google-chrome-stable
   ```

2. **Install Python dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run headless scraper:**
   ```bash
   python3 run_headless.py
   ```

### **Setting up Automated Scheduling**

```bash
# Edit crontab
crontab -e

# Add one of these lines:

# Every 30 minutes (RECOMMENDED)
*/30 * * * * cd /path/to/scraper && python3 run_headless.py

# Every hour at minute 0
0 * * * * cd /path/to/scraper && python3 run_headless.py

# Every 6 hours
0 */6 * * * cd /path/to/scraper && python3 run_headless.py
```

### **Monitor Your Server**

```bash
# View live logs
tail -f appointment_scraper.log

# View all logs
cat appointment_scraper.log

# Check cron job status
crontab -l
```

### **Server Logs**

The headless mode creates detailed logs in `appointment_scraper.log`:

```
2025-06-01 13:57:50,732 - INFO - 🇩🇪 Berlin Appointment Scraper - Headless Mode
2025-06-01 13:57:50,732 - INFO - ⏰ Started at: 2025-06-01 13:57:50
2025-06-01 13:57:58,773 - INFO - 💤 No appointments available
2025-06-01 13:57:58,773 - INFO - ✅ Check completed at: 2025-06-01 13:57:58
```

## Testing

The project includes comprehensive tests to ensure reliability:

### **Running Tests**

```bash
# Using Makefile (recommended)
make test

# Manual execution
python3 -m pytest tests/ -v

# Run tests in watch mode (reruns on file changes)
make test-watch
```

### **Test Coverage**

The test suite covers:
- ✅ **Scraper initialization** and configuration
- ✅ **Driver setup** and fallback mechanisms  
- ✅ **Appointment checking** logic
- ✅ **Error handling** for various scenarios
- ✅ **Configuration validation**
- ✅ **Integration testing**

### **Test Structure**

```
tests/
├── __init__.py
├── test_scraper.py     # Main scraper functionality tests
└── test_config.py      # Configuration tests
```

## Configuration

Edit `config.py` to customize the scraper:

- `headless_mode`: Set to `False` to see the browser in action
- `wait_timeout`: Adjust timeout for element loading
- `page_load_delay`: Adjust delay after form submission

## Notification Setup

To enable notifications when appointments are found:

1. **Uncomment the notification code** in `berlin_appointment_scraper.py` in the `send_notification` method
2. **Replace `YOUR_NOTIFICATION_ENDPOINT_HERE`** with your actual endpoint URL
3. **Customize the payload** as needed for your notification service

Example notification payload:
```python
payload = {
    "message": message,
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    "source": "Berlin Appointment Scraper"
}
```

## How It Works

1. **Navigates** to the Berlin service page for citizenship test appointments
2. **Selects** the "Alle Standorte auswählen" checkbox to check all locations
3. **Clicks** the submit button to proceed to appointment selection
4. **Checks** if the page contains the "no appointments available" message
5. **Triggers notification** if appointments are found

## Key Features for Server Deployment

- ✅ **Fully headless** - no display required
- ✅ **Automatic Chrome detection** for Linux/macOS
- ✅ **Comprehensive logging** to `appointment_scraper.log`
- ✅ **Server-optimized Chrome options** (disabled images, extensions, etc.)
- ✅ **Error handling** with fallback ChromeDriver setup
- ✅ **Easy installation script** for Ubuntu/Debian servers

## Output

The scraper provides clear console output:

```
==================================================
🇩🇪 Berlin Appointment Scraper
==================================================
🚀 Starting Berlin appointment check...
📱 Navigating to: https://service.berlin.de/dienstleistung/351180/
🔍 Looking for 'Alle Standorte auswählen' checkbox...
✅ Selecting 'Alle Standorte auswählen' checkbox...
🔍 Looking for submit button...
🔄 Clicking submit button...
⏳ Waiting for results page to load...
❌ No appointments available
🔒 Browser closed

💤 Check completed - No appointments available
==================================================
```

## Scheduling

This scraper is designed to be run on a schedule. You can use:

- **Cron jobs** (Linux/macOS)
- **Task Scheduler** (Windows)
- **GitHub Actions** (Cloud)
- **Cloud functions** (AWS Lambda, Google Cloud Functions, etc.)

Example cron job to run every 30 minutes:
```bash
*/30 * * * * /usr/bin/python3 /path/to/berlin_appointment_scraper.py
```

## Error Handling

The scraper includes comprehensive error handling for:

- ⏰ Page load timeouts
- ❌ Missing elements
- 🔗 Network issues
- 🚫 Unexpected page changes

## Troubleshooting

### **Common Issues**

#### **ChromeDriver Issues**
If you see errors like "Exec format error" with ChromeDriver:
```bash
# The scraper automatically handles this with fallback mechanisms
# If issues persist, try:
make clean
rm -rf ~/.wdm  # Clear webdriver-manager cache
make run-test  # Try again
```

#### **Python 3.13 + lxml Issues**
```bash
# lxml compilation fails on Python 3.13
# Solution: The scraper works without lxml (already handled in requirements.txt)
# No action needed - the scraper will work fine
```

#### **Permission Issues on macOS**
```bash
# If Chrome security warnings appear:
# Allow Chrome in System Preferences > Security & Privacy
# Or run in headless mode: make run-headless
```

#### **No Appointments Found**
```bash
# This is normal - the scraper is working correctly
# Appointments are rare and get booked quickly
# Set up automated checking: make cron-setup
```

### **Debug Mode**

For debugging, use the test mode with visible browser:
```bash
make run-test
# or
python3 test_scraper.py
```

### **Logs**

Check logs for detailed information:
```bash
make logs        # Recent logs
make logs-tail   # Live log monitoring
```

## Customization

### Adding More Check Criteria

You can extend the scraper to check for specific appointment types or locations by modifying the logic in the `check_appointments` method.

### Different Notification Methods

The notification system can be adapted for:

- 📧 Email notifications
- 📱 SMS/Push notifications
- 💬 Slack/Discord webhooks
- 📞 Phone calls

## Legal and Ethical Considerations

- ⚖️ Use responsibly and respect the website's terms of service
- 🕒 Don't run too frequently to avoid overloading the server
- 🤝 This tool is for personal use only

## Troubleshooting

### Common Issues

1. **ChromeDriver issues**: The script automatically manages ChromeDriver, but ensure Chrome is installed
   - On macOS: The script will automatically fall back to system ChromeDriver if webdriver-manager fails
   - Make sure Google Chrome is installed in `/Applications/Google Chrome.app`

2. **Element not found**: The website structure may have changed; check the selectors in `config.py`

3. **Timeout errors**: Increase the `wait_timeout` in `config.py`

4. **Click interception errors**: The script handles sticky overlays automatically with JavaScript clicks

5. **Python command not found**: 
   - On macOS/Linux: Use `python3` instead of `python`
   - On Windows: Use `python` or `py`

### Debug Mode

Set `headless_mode = False` in `config.py` to see the browser in action and debug issues.

### macOS Specific Notes

- The scraper automatically sets the Chrome binary path for macOS
- If webdriver-manager fails, it falls back to system ChromeDriver
- Use `python3` and `pip3` commands on macOS

## Files Structure

```
├── berlin_appointment_scraper.py  # Main scraper script
├── config.py                     # Configuration settings
├── requirements.txt               # Python dependencies
└── README.md                     # This file
```

## Contributing

Feel free to improve this scraper by:

- Adding more robust error handling
- Implementing additional notification methods
- Optimizing performance
- Adding more configuration options

## Disclaimer

This tool is for educational and personal use only. Use it responsibly and in accordance with the website's terms of service. 