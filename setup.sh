#!/bin/bash
# Setup script for voice-clone-cli development environment

set -e  # Exit on error

echo "🚀 Setting up voice-clone-cli development environment..."

# Check Python version
echo "📋 Checking Python version..."
if ! command -v python3.10 &> /dev/null; then
    echo "❌ Python 3.10 not found. Please install Python 3.10 first."
    echo "   You can use pyenv: pyenv install 3.10"
    exit 1
fi

PYTHON_VERSION=$(python3.10 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
if [ "$PYTHON_VERSION" != "3.10" ]; then
    echo "⚠️  Warning: Python 3.10 is recommended, but found $PYTHON_VERSION"
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping creation."
else
    python3.10 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install development dependencies
echo "📚 Installing development dependencies..."
pip install pre-commit black ruff mypy pytest pytest-cov

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
pre-commit install
pre-commit install --hook-type commit-msg
pre-commit install --hook-type pre-push

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To deactivate, run:"
echo "  deactivate"
echo ""
echo "Happy coding! 🎉"
