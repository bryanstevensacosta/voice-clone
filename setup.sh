#!/bin/bash
# Setup script for TTS Studio development environment (Monorepo)

set -e  # Exit on error

echo "🚀 Setting up TTS Studio development environment..."
echo ""

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

# Navigate to core library
echo "📂 Navigating to apps/core/..."
cd apps/core

# Create virtual environment
echo "📦 Creating virtual environment in apps/core/venv/..."
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

# Install package in development mode
echo "📚 Installing TTS Studio core library..."
pip install -e ".[dev]"

# Navigate back to root for pre-commit hooks
cd ../..

# Install pre-commit hooks (repository-wide)
echo "🪝 Installing pre-commit hooks..."
pre-commit install
pre-commit install --hook-type commit-msg
pre-commit install --hook-type pre-push
pre-commit install --hook-type pre-merge-commit

echo ""
echo "✅ Setup complete!"
echo ""
echo "📍 Virtual environment location: apps/core/venv/"
echo ""
echo "To activate the virtual environment, run:"
echo "  cd apps/core"
echo "  source venv/bin/activate"
echo ""
echo "To run tests:"
echo "  cd apps/core"
echo "  pytest"
echo ""
echo "To deactivate:"
echo "  deactivate"
echo ""
echo "Happy coding! 🎉"
