.PHONY: help install test run-test run-headless run-basic clean setup-venv lint format check-deps logs cron-setup cron-stop

# Default target
help:
	@echo "🇩🇪 Berlin Appointment Scraper - Available Commands:"
	@echo "================================================"
	@echo "setup-venv     - Create and setup virtual environment"
	@echo "install        - Install dependencies"
	@echo "install-dev    - Install dev dependencies including tests"
	@echo "run-basic      - Run scraper in visible mode"
	@echo "run-test       - Run scraper in test mode (visible browser)"
	@echo "run-headless   - Run scraper in headless mode"
	@echo "test           - Run all tests"
	@echo "test-watch     - Run tests in watch mode"
	@echo "lint           - Run linting checks"
	@echo "format         - Format code"
	@echo "check-deps     - Check for dependency issues"
	@echo "logs           - Show recent logs"
	@echo "logs-tail      - Tail logs in real-time"
	@echo "clean          - Clean up temporary files"
	@echo "cron-setup     - Setup cron job for automated runs"
	@echo "cron-stop      - Remove cron job"
	@echo "server-install - Install Chrome on Ubuntu/Debian server"

# Virtual environment setup
setup-venv:
	@echo "🔧 Setting up virtual environment..."
	python3 -m venv venv
	@echo "✅ Virtual environment created!"
	@echo "💡 Activate with: source venv/bin/activate"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip3 install --upgrade pip
	pip3 install -r requirements.txt
	@echo "✅ Dependencies installed!"

install-dev: install
	@echo "📦 Installing development dependencies..."
	pip3 install pytest==8.0.0 pytest-mock==3.12.0 black==24.0.0 flake8==7.0.0
	@echo "✅ Development dependencies installed!"

# Run commands
run-basic:
	@echo "🚀 Running Berlin Appointment Scraper (Basic Mode)..."
	python3 berlin_appointment_scraper.py

run-test:
	@echo "🧪 Running Berlin Appointment Scraper (Test Mode - Visible Browser)..."
	python3 test_scraper.py

run-headless:
	@echo "🤖 Running Berlin Appointment Scraper (Headless Mode)..."
	python3 run_headless.py

# Testing
test:
	@echo "🧪 Running tests..."
	python3 -m pytest tests/ -v

test-watch:
	@echo "🧪 Running tests in watch mode..."
	python3 -m pytest tests/ -v --tb=short -f

# Code quality
lint:
	@echo "🔍 Running linting checks..."
	python3 -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	python3 -m flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:
	@echo "🎨 Formatting code..."
	python3 -m black . --line-length=100
	@echo "✅ Code formatted!"

# Dependency management
check-deps:
	@echo "🔍 Checking dependencies..."
	pip3 check
	pip3 list --outdated

# Logs
logs:
	@echo "📋 Recent logs:"
	@if [ -f appointment_scraper.log ]; then tail -20 appointment_scraper.log; else echo "No logs found"; fi

logs-tail:
	@echo "📋 Tailing logs (Ctrl+C to stop):"
	@if [ -f appointment_scraper.log ]; then tail -f appointment_scraper.log; else echo "No logs found"; fi

# Cleanup
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache/
	rm -rf build/
	rm -rf dist/
	@echo "✅ Cleanup complete!"

# Cron setup
cron-setup:
	@echo "⏰ Setting up cron job..."
	@current_dir=$$(pwd); \
	echo "*/30 * * * * cd $$current_dir && source venv/bin/activate && python3 run_headless.py" | crontab -
	@echo "✅ Cron job set up to run every 30 minutes"
	@echo "💡 View with: crontab -l"

cron-stop:
	@echo "⏰ Removing cron job..."
	@crontab -r 2>/dev/null || true
	@echo "✅ Cron job removed"

# Server installation (Ubuntu/Debian)
server-install:
	@echo "🖥️ Installing Chrome on Ubuntu/Debian server..."
	chmod +x install_server.sh
	./install_server.sh
	@echo "✅ Server installation complete!"

# Quick development setup
dev-setup: setup-venv install-dev
	@echo "🚀 Development environment ready!"
	@echo "💡 Activate venv: source venv/bin/activate"
	@echo "💡 Run tests: make test"
	@echo "💡 Run scraper: make run-test" 