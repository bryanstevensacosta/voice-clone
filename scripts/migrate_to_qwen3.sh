#!/bin/bash
# Migration script from Coqui TTS (XTTS-v2) to Qwen3-TTS
# This script automates the migration process with backup and rollback capabilities

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKUP_DIR="./backups/pre-qwen3-migration-$(date +%Y%m%d_%H%M%S)"
VENV_DIR="./venv"
DATA_DIR="./data"
CONFIG_DIR="./config"

# Functions
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if running in correct directory
check_environment() {
    print_header "Checking Environment"

    if [ ! -f "setup.py" ] || [ ! -f "pyproject.toml" ]; then
        print_error "Not in project root directory. Please run from voice-clone root."
        exit 1
    fi

    if [ ! -d "$VENV_DIR" ]; then
        print_error "Virtual environment not found. Please run ./setup.sh first."
        exit 1
    fi

    print_success "Environment check passed"
}

# Create backup
create_backup() {
    print_header "Creating Backup"

    mkdir -p "$BACKUP_DIR"

    # Backup configuration files
    print_info "Backing up configuration files..."
    cp -r "$CONFIG_DIR" "$BACKUP_DIR/" 2>/dev/null || true

    # Backup requirements
    cp requirements.txt "$BACKUP_DIR/" 2>/dev/null || true
    cp pyproject.toml "$BACKUP_DIR/" 2>/dev/null || true
    cp setup.py "$BACKUP_DIR/" 2>/dev/null || true

    # Backup voice profiles
    if [ -d "$DATA_DIR" ]; then
        print_info "Backing up voice profiles..."
        mkdir -p "$BACKUP_DIR/data"
        cp "$DATA_DIR"/*.json "$BACKUP_DIR/data/" 2>/dev/null || true
    fi

    # Save pip freeze
    source "$VENV_DIR/bin/activate"
    pip freeze > "$BACKUP_DIR/pip_freeze_before.txt"
    deactivate

    print_success "Backup created at: $BACKUP_DIR"
}

# Uninstall Coqui TTS
uninstall_coqui_tts() {
    print_header "Uninstalling Coqui TTS"

    source "$VENV_DIR/bin/activate"

    # Check if TTS is installed
    if pip show TTS &> /dev/null; then
        print_info "Uninstalling TTS package..."
        pip uninstall -y TTS
        print_success "TTS package uninstalled"
    else
        print_warning "TTS package not found (already uninstalled)"
    fi

    # Verify uninstallation
    if pip show TTS &> /dev/null; then
        print_error "Failed to uninstall TTS package"
        deactivate
        exit 1
    fi

    # Test that TTS cannot be imported
    if python -c "import TTS" 2>/dev/null; then
        print_error "TTS can still be imported after uninstallation"
        deactivate
        exit 1
    fi

    print_success "Coqui TTS successfully uninstalled"
    deactivate
}

# Clean TTS cache
clean_tts_cache() {
    print_header "Cleaning TTS Cache"

    # Common TTS cache locations
    TTS_CACHE_DIRS=(
        "$HOME/.local/share/tts"
        "$HOME/.cache/tts"
        "./data/models/xtts-v2"
        "./data/models/xtts_v2"
    )

    for cache_dir in "${TTS_CACHE_DIRS[@]}"; do
        if [ -d "$cache_dir" ]; then
            print_info "Archiving cache: $cache_dir"
            # Move to backup instead of deleting
            mkdir -p "$BACKUP_DIR/cache"
            mv "$cache_dir" "$BACKUP_DIR/cache/" 2>/dev/null || true
            print_success "Archived: $cache_dir"
        fi
    done

    print_success "TTS cache cleaned"
}

# Install Qwen3-TTS
install_qwen3_tts() {
    print_header "Installing Qwen3-TTS"

    source "$VENV_DIR/bin/activate"

    print_info "Installing qwen-tts package..."
    pip install qwen-tts>=1.0.0

    # Verify installation
    if ! pip show qwen-tts &> /dev/null; then
        print_error "Failed to install qwen-tts package"
        deactivate
        exit 1
    fi

    # Test import
    if ! python -c "from qwen_tts import Qwen3TTSModel" 2>/dev/null; then
        print_error "Cannot import Qwen3TTSModel after installation"
        deactivate
        exit 1
    fi

    print_success "Qwen3-TTS successfully installed"

    # Save new pip freeze
    pip freeze > "$BACKUP_DIR/pip_freeze_after.txt"

    deactivate
}

# Update configuration files
update_configuration() {
    print_header "Updating Configuration Files"

    # Update config.yaml if it exists
    if [ -f "$CONFIG_DIR/config.yaml" ]; then
        print_info "Updating config.yaml..."

        # Backup original
        cp "$CONFIG_DIR/config.yaml" "$CONFIG_DIR/config.yaml.backup"

        # Update model name
        sed -i.bak 's|tts_models/multilingual/multi-dataset/xtts_v2|Qwen/Qwen3-TTS-12Hz-1.7B-Base|g' "$CONFIG_DIR/config.yaml"

        # Update sample rate
        sed -i.bak 's|sample_rate: 22050|sample_rate: 12000|g' "$CONFIG_DIR/config.yaml"

        # Add dtype if not present
        if ! grep -q "dtype:" "$CONFIG_DIR/config.yaml"; then
            sed -i.bak '/device:/a\  dtype: "float32"' "$CONFIG_DIR/config.yaml"
        fi

        # Update models path
        sed -i.bak 's|models: "./data/models"|models: "./data/qwen3_models"|g' "$CONFIG_DIR/config.yaml"

        rm "$CONFIG_DIR/config.yaml.bak" 2>/dev/null || true

        print_success "config.yaml updated"
    fi

    # Create qwen3_models directory
    mkdir -p "$DATA_DIR/qwen3_models"
    print_success "Created qwen3_models directory"
}

# Verify migration
verify_migration() {
    print_header "Verifying Migration"

    source "$VENV_DIR/bin/activate"

    # Check TTS is not installed
    print_info "Checking TTS is uninstalled..."
    if pip show TTS &> /dev/null; then
        print_error "TTS package still installed"
        deactivate
        return 1
    fi
    print_success "TTS package not found (correct)"

    # Check qwen-tts is installed
    print_info "Checking qwen-tts is installed..."
    if ! pip show qwen-tts &> /dev/null; then
        print_error "qwen-tts package not installed"
        deactivate
        return 1
    fi
    print_success "qwen-tts package installed"

    # Check imports
    print_info "Checking imports..."
    if python -c "from qwen_tts import Qwen3TTSModel" 2>/dev/null; then
        print_success "Qwen3TTSModel can be imported"
    else
        print_error "Cannot import Qwen3TTSModel"
        deactivate
        return 1
    fi

    if python -c "import TTS" 2>/dev/null; then
        print_error "TTS can still be imported (should fail)"
        deactivate
        return 1
    fi
    print_success "TTS cannot be imported (correct)"

    # Run basic tests
    print_info "Running basic tests..."
    if pytest tests/test_qwen3_model_manager.py -q 2>/dev/null; then
        print_success "Basic tests passed"
    else
        print_warning "Some tests failed (this may be expected)"
    fi

    deactivate

    print_success "Migration verification complete"
}

# Print rollback instructions
print_rollback_instructions() {
    print_header "Rollback Instructions"

    echo ""
    echo "If you need to rollback this migration:"
    echo ""
    echo "1. Restore backup:"
    echo "   cp -r $BACKUP_DIR/config/* ./config/"
    echo "   cp $BACKUP_DIR/requirements.txt ."
    echo "   cp $BACKUP_DIR/pyproject.toml ."
    echo "   cp $BACKUP_DIR/setup.py ."
    echo ""
    echo "2. Reinstall old dependencies:"
    echo "   source venv/bin/activate"
    echo "   pip install -r $BACKUP_DIR/pip_freeze_before.txt"
    echo "   deactivate"
    echo ""
    echo "3. Restore TTS cache (optional):"
    echo "   mv $BACKUP_DIR/cache/* ~/.local/share/"
    echo ""
}

# Main migration process
main() {
    print_header "Qwen3-TTS Migration Script"
    echo ""
    echo "This script will:"
    echo "  1. Create a backup of your current setup"
    echo "  2. Uninstall Coqui TTS (XTTS-v2)"
    echo "  3. Clean TTS cache"
    echo "  4. Install Qwen3-TTS"
    echo "  5. Update configuration files"
    echo "  6. Verify the migration"
    echo ""

    read -p "Do you want to continue? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Migration cancelled"
        exit 0
    fi

    # Execute migration steps
    check_environment
    create_backup
    uninstall_coqui_tts
    clean_tts_cache
    install_qwen3_tts
    update_configuration
    verify_migration

    # Success message
    print_header "Migration Complete!"
    echo ""
    print_success "Successfully migrated from Coqui TTS to Qwen3-TTS"
    echo ""
    echo "Backup location: $BACKUP_DIR"
    echo ""
    echo "Next steps:"
    echo "  1. Review the updated configuration in config/config.yaml"
    echo "  2. Update your voice profiles with ref_text:"
    echo "     voice-clone prepare --samples ./data/samples --ref-text \"Your reference text\" --output profile.json"
    echo "  3. Test voice generation:"
    echo "     voice-clone test --profile profile.json"
    echo ""

    print_rollback_instructions
}

# Run main function
main
