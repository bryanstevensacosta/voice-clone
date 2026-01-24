.PHONY: help setup install clean test lint format type-check pre-commit run

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup:  ## Set up development environment (creates venv and installs dependencies)
	@echo "🚀 Setting up development environment..."
	@./setup.sh

install:  ## Install project in development mode
	@echo "📦 Installing project in development mode..."
	@pip install -e ".[dev]"

clean:  ## Clean up generated files
	@echo "🧹 Cleaning up..."
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info
	@rm -rf .pytest_cache/
	@rm -rf .mypy_cache/
	@rm -rf .ruff_cache/
	@rm -rf htmlcov/
	@rm -rf .coverage
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete"

test:  ## Run tests with coverage
	@echo "🧪 Running tests..."
	@pytest tests/ --cov=voice_clone --cov-report=term-missing --cov-report=html

test-fast:  ## Run tests without coverage
	@echo "🧪 Running tests (fast)..."
	@pytest tests/ -v

lint:  ## Run linter (Ruff)
	@echo "🔍 Running linter..."
	@ruff check src/ tests/

format:  ## Format code with Black
	@echo "✨ Formatting code..."
	@black src/ tests/

type-check:  ## Run type checker (MyPy)
	@echo "🔎 Running type checker..."
	@mypy src/

pre-commit:  ## Run all pre-commit hooks
	@echo "🪝 Running pre-commit hooks..."
	@pre-commit run --all-files

pre-commit-update:  ## Update pre-commit hooks
	@echo "⬆️  Updating pre-commit hooks..."
	@pre-commit autoupdate

rebase-master:  ## Rebase current branch on master
	@echo "🔄 Rebasing on master..."
	@git fetch origin
	@git rebase origin/master

rebase-main:  ## Rebase current branch on main
	@echo "🔄 Rebasing on main..."
	@git fetch origin
	@git rebase origin/main

rebase-develop:  ## Rebase current branch on develop
	@echo "🔄 Rebasing on develop..."
	@git fetch origin
	@git rebase origin/develop

sync:  ## Fetch and show status
	@echo "📡 Fetching latest changes..."
	@git fetch origin
	@echo ""
	@echo "📊 Current status:"
	@git status -sb

check-branch:  ## Check if current branch needs rebase
	@echo "🔍 Checking branch status..."
	@./scripts/check-rebase-before-push.sh || true

check-terraform:  ## Check if Terraform state is in sync with remote
	@echo "🔍 Checking Terraform state..."
	@./scripts/check-terraform-sync.sh

terraform-plan:  ## Run terraform plan
	@echo "📋 Running terraform plan..."
	@cd terraform && terraform plan

terraform-apply:  ## Apply terraform changes
	@echo "🚀 Applying terraform changes..."
	@cd terraform && terraform apply

terraform-init:  ## Initialize terraform
	@echo "🔧 Initializing terraform..."
	@cd terraform && terraform init

venv:  ## Create virtual environment
	@echo "📦 Creating virtual environment..."
	@python3.10 -m venv venv
	@echo "✅ Virtual environment created"
	@echo "Activate it with: source venv/bin/activate"

activate:  ## Show activation command
	@echo "To activate the virtual environment, run:"
	@echo "  source venv/bin/activate"

dev:  ## Run in development mode
	@echo "🔧 Starting development mode..."
	@python -m voice_clone.cli --help

.DEFAULT_GOAL := help
