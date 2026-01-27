#!/bin/bash

# Pre-push hook to ensure code is formatted before pushing
# This prevents CI failures due to formatting issues

set -e

echo "🔍 Checking code formatting before push..."

# Check if black would reformat any files
if ! black --check src/ tests/ 2>&1 | grep -q "would be left unchanged"; then
    echo ""
    echo "❌ Error: Code is not properly formatted with Black"
    echo ""
    echo "Files that need formatting:"
    black --check src/ tests/ 2>&1 | grep "would reformat" || true
    echo ""
    echo "💡 To fix this, run:"
    echo "   black src/ tests/"
    echo ""
    echo "Or run all pre-commit hooks:"
    echo "   pre-commit run --all-files"
    echo ""
    exit 1
fi

# Check if ruff would make any changes
if ! ruff check src/ tests/ --exit-zero > /dev/null 2>&1; then
    echo ""
    echo "⚠️  Warning: Ruff found issues that can be auto-fixed"
    echo ""
    echo "💡 To fix this, run:"
    echo "   ruff check src/ tests/ --fix"
    echo ""
    echo "Or run all pre-commit hooks:"
    echo "   pre-commit run --all-files"
    echo ""
    # Don't exit, just warn
fi

echo "✅ Code formatting check passed!"
echo ""
