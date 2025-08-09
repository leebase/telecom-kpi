# Makefile for Telecom KPI Dashboard

# Variables
PYTHON := python
PIP := pip
VENV := venv
STREAMLIT := streamlit
PYTEST := pytest
SPHINX := sphinx-build
BANDIT := bandit
SAFETY := safety

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
RED := \033[0;31m
YELLOW := \033[1;33m
NC := \033[0m # No Color

.PHONY: help install install-dev install-security setup run test test-unit test-integration test-coverage lint security-scan docs docs-serve clean clean-all check-env validate

# Default target
help: ## Show this help message
	@echo "$(BLUE)Telecom KPI Dashboard - Development Makefile$(NC)"
	@echo ""
	@echo "$(GREEN)Available targets:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(BLUE)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Installation targets
install: ## Install core dependencies
	@echo "$(GREEN)Installing core dependencies...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

install-dev: install ## Install development dependencies
	@echo "$(GREEN)Installing development dependencies...$(NC)"
	$(PIP) install -r requirements-dev.txt
	pre-commit install

install-security: ## Install security dependencies
	@echo "$(GREEN)Installing security dependencies...$(NC)"
	$(PIP) install -r requirements-security.txt

install-all: install install-dev install-security ## Install all dependencies

# Setup targets
setup: install-all ## Complete project setup
	@echo "$(GREEN)Setting up project...$(NC)"
	$(PYTHON) setup_secure_environment.py
	@echo "$(GREEN)Setup complete!$(NC)"

setup-env: ## Create virtual environment
	@echo "$(GREEN)Creating virtual environment...$(NC)"
	$(PYTHON) -m venv $(VENV)
	@echo "$(YELLOW)Activate with: source venv/bin/activate$(NC)"

# Running targets
run: check-env ## Run the Streamlit application
	@echo "$(GREEN)Starting Telecom KPI Dashboard...$(NC)"
	$(STREAMLIT) run app.py

run-dev: check-env ## Run in development mode with debug info
	@echo "$(GREEN)Starting in development mode...$(NC)"
	DEBUG=1 $(STREAMLIT) run app.py --server.runOnSave true

run-prod: check-env ## Run in production mode
	@echo "$(GREEN)Starting in production mode...$(NC)"
	$(STREAMLIT) run app.py --server.port 8501 --server.address 0.0.0.0

# Testing targets
test: ## Run all tests
	@echo "$(GREEN)Running all tests...$(NC)"
	$(PYTEST) tests/ -v

test-unit: ## Run unit tests only
	@echo "$(GREEN)Running unit tests...$(NC)"
	$(PYTEST) tests/unit/ -v -m unit

test-integration: ## Run integration tests only
	@echo "$(GREEN)Running integration tests...$(NC)"
	$(PYTEST) tests/integration/ -v -m integration

test-coverage: ## Run tests with coverage report
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	$(PYTEST) tests/ -v --cov=src --cov=. --cov-report=html --cov-report=term-missing --cov-report=xml

test-performance: ## Run performance tests
	@echo "$(GREEN)Running performance tests...$(NC)"
	$(PYTEST) tests/ -v -m performance

test-security: ## Run security tests
	@echo "$(GREEN)Running security tests...$(NC)"
	$(PYTEST) tests/ -v -m security

test-watch: ## Run tests in watch mode
	@echo "$(GREEN)Running tests in watch mode...$(NC)"
	$(PYTEST) tests/ -v --looponfail

# Quality assurance targets
lint: ## Run code linting
	@echo "$(GREEN)Running linting...$(NC)"
	flake8 src/ tests/ *.py --max-line-length=100 --ignore=E203,W503
	black --check src/ tests/ *.py
	isort --check-only src/ tests/ *.py

lint-fix: ## Fix linting issues automatically
	@echo "$(GREEN)Fixing linting issues...$(NC)"
	black src/ tests/ *.py
	isort src/ tests/ *.py

type-check: ## Run type checking
	@echo "$(GREEN)Running type checking...$(NC)"
	mypy src/ --ignore-missing-imports

# Security targets
security-scan: ## Run security scans
	@echo "$(GREEN)Running security scans...$(NC)"
	$(BANDIT) -r . -f json -o reports/bandit_report.json || true
	$(SAFETY) check --json --output reports/safety_report.json || true
	@echo "$(GREEN)Security reports generated in reports/$(NC)"

security-check: ## Quick security check
	@echo "$(GREEN)Running quick security check...$(NC)"
	$(BANDIT) -r src/ -ll
	$(SAFETY) check

# Documentation targets
docs: ## Build documentation
	@echo "$(GREEN)Building documentation...$(NC)"
	mkdir -p docs/build
	$(SPHINX) -b html docs/source docs/build/html
	@echo "$(GREEN)Documentation built in docs/build/html/$(NC)"

docs-serve: docs ## Build and serve documentation locally
	@echo "$(GREEN)Serving documentation at http://localhost:8000$(NC)"
	cd docs/build/html && $(PYTHON) -m http.server 8000

docs-clean: ## Clean documentation build
	@echo "$(GREEN)Cleaning documentation build...$(NC)"
	rm -rf docs/build/

docs-autobuild: ## Auto-rebuild documentation on changes
	@echo "$(GREEN)Auto-building documentation...$(NC)"
	sphinx-autobuild docs/source docs/build/html --host 0.0.0.0 --port 8001

# Database targets
db-setup: ## Set up database
	@echo "$(GREEN)Setting up database...$(NC)"
	$(PYTHON) setup_database.py

db-load: ## Load sample data
	@echo "$(GREEN)Loading sample data...$(NC)"
	$(PYTHON) load_data.py

db-generate: ## Generate test data
	@echo "$(GREEN)Generating test data...$(NC)"
	$(PYTHON) generate_comprehensive_data.py

db-reset: db-setup db-load ## Reset database with fresh data
	@echo "$(GREEN)Database reset complete!$(NC)"

# Utility targets
clean: ## Clean temporary files
	@echo "$(GREEN)Cleaning temporary files...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -delete
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/

clean-all: clean docs-clean ## Clean all generated files
	@echo "$(GREEN)Cleaning all generated files...$(NC)"
	rm -rf $(VENV)/
	rm -rf logs/
	rm -rf reports/

format: ## Format code
	@echo "$(GREEN)Formatting code...$(NC)"
	black src/ tests/ *.py
	isort src/ tests/ *.py

check-env: ## Check if environment variable is set
	@if [ -z "$$LLM_API_KEY" ]; then \
		echo "$(RED)Error: LLM_API_KEY environment variable not set$(NC)"; \
		echo "$(YELLOW)Set it with: export LLM_API_KEY='your-api-key'$(NC)"; \
		exit 1; \
	fi

validate: lint type-check test security-check ## Run all validation checks
	@echo "$(GREEN)All validation checks passed!$(NC)"

# Deployment targets
package: validate ## Package for deployment
	@echo "$(GREEN)Packaging application...$(NC)"
	$(PYTHON) setup.py sdist bdist_wheel

docker-build: ## Build Docker image
	@echo "$(GREEN)Building Docker image...$(NC)"
	docker build -t telecom-dashboard:latest .

docker-run: docker-build ## Build and run Docker container
	@echo "$(GREEN)Running Docker container...$(NC)"
	docker run -p 8501:8501 -e LLM_API_KEY="$$LLM_API_KEY" telecom-dashboard:latest

docker-compose-up: ## Start with Docker Compose
	@echo "$(GREEN)Starting with Docker Compose...$(NC)"
	docker-compose up -d

docker-compose-down: ## Stop Docker Compose
	@echo "$(GREEN)Stopping Docker Compose...$(NC)"
	docker-compose down

# Monitoring targets
logs: ## Show application logs
	@echo "$(GREEN)Showing application logs...$(NC)"
	tail -f logs/app.log

logs-security: ## Show security logs
	@echo "$(GREEN)Showing security logs...$(NC)"
	tail -f logs/security.log

monitor: ## Monitor application performance
	@echo "$(GREEN)Monitoring application...$(NC)"
	$(PYTHON) -c "
import time
import psutil
import requests
while True:
    try:
        response = requests.get('http://localhost:8501', timeout=5)
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        print(f'Status: {response.status_code}, CPU: {cpu}%, Memory: {memory}%')
    except Exception as e:
        print(f'Error: {e}')
    time.sleep(10)
"

# Development workflow targets
dev-setup: setup-env install-all setup ## Complete development setup
	@echo "$(GREEN)Development environment ready!$(NC)"

dev-test: lint test-coverage ## Run development tests
	@echo "$(GREEN)Development tests complete!$(NC)"

dev-deploy: validate package ## Prepare for deployment
	@echo "$(GREEN)Ready for deployment!$(NC)"

# Report generation
reports: ## Generate all reports
	@echo "$(GREEN)Generating reports...$(NC)"
	mkdir -p reports
	$(PYTEST) tests/ --cov=src --cov-report=html:reports/coverage
	$(BANDIT) -r . -f html -o reports/security.html || true
	@echo "$(GREEN)Reports generated in reports/$(NC)"

# Benchmarking
benchmark: ## Run performance benchmarks
	@echo "$(GREEN)Running performance benchmarks...$(NC)"
	$(PYTHON) -m pytest tests/ -v -m performance --benchmark-only

# Information targets
info: ## Show project information
	@echo "$(BLUE)Telecom KPI Dashboard$(NC)"
	@echo "Version: 1.0.0"
	@echo "Python: $$(python --version)"
	@echo "Virtual Env: $$(which python)"
	@echo "Dependencies: $$(pip list | wc -l) packages installed"
	@echo "Tests: $$(find tests/ -name 'test_*.py' | wc -l) test files"
	@echo "Source Files: $$(find src/ -name '*.py' | wc -l) Python files"

# Quick shortcuts
t: test ## Quick test shortcut
l: lint ## Quick lint shortcut  
r: run ## Quick run shortcut
c: clean ## Quick clean shortcut
d: docs ## Quick docs shortcut


