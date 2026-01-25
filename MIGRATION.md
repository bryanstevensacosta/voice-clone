# Migration Guide: Coqui TTS (XTTS-v2) to Qwen3-TTS

This guide provides detailed instructions for migrating from Coqui TTS (XTTS-v2) to Qwen3-TTS.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Automated Migration](#automated-migration)
- [Manual Migration](#manual-migration)
- [Post-Migration Steps](#post-migration-steps)
- [Rollback Procedure](#rollback-procedure)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)

## Overview

### What's Changing

| Component | Before (XTTS-v2) | After (Qwen3-TTS) |
|-----------|------------------|-------------------|
| **Package** | `TTS>=0.22.0` | `qwen-tts>=1.0.0` |
| **Model** | `tts_models/multilingual/multi-dataset/xtts_v2` | `Qwen/Qwen3-TTS-12Hz-1.7B-Base` |
| **Sample Rate** | 22050 Hz | 12000 Hz |
| **Device** | CUDA/CPU | MPS/CPU (Apple Silicon optimized) |
| **Dtype** | auto | float32 (required for MPS) |
| **Samples Required** | 6-10 samples | 1-3 samples |
| **Model Size** | ~1.8GB | ~3.4GB |

### Why Migrate?

- **Better Apple Silicon Support**: Native MPS optimization
- **Fewer Samples Required**: 1-3 samples vs 6-10
- **Improved Quality**: Better voice cloning with less data
- **Active Development**: Qwen3-TTS is actively maintained

## Prerequisites

Before starting the migration:

1. **Backup your data**:
   ```bash
   # Backup voice profiles
   cp -r data/samples data/samples_backup_$(date +%Y%m%d)
   cp data/*.json data/backups/

   # Backup configuration
   cp -r config config_backup_$(date +%Y%m%d)
   ```

2. **Ensure you have**:
   - Python 3.9-3.11
   - Virtual environment activated
   - At least 10GB free disk space
   - Stable internet connection (for model download)

3. **Save current state**:
   ```bash
   pip freeze > requirements_before_migration.txt
   ```

## Automated Migration

### Option 1: Using Migration Script (Recommended)

The automated script handles everything for you:

```bash
# Run the migration script
./scripts/migrate_to_qwen3.sh
```

The script will:
1. ✅ Create a backup of your current setup
2. ✅ Uninstall Coqui TTS
3. ✅ Clean TTS cache
4. ✅ Install Qwen3-TTS
5. ✅ Update configuration files
6. ✅ Verify the migration

**Estimated time**: 5-10 minutes

### What the Script Does

#### 1. Backup Creation
- Backs up `config/`, `requirements.txt`, `pyproject.toml`, `setup.py`
- Backs up voice profiles (`data/*.json`)
- Saves `pip freeze` output
- Creates backup in `./backups/pre-qwen3-migration-YYYYMMDD_HHMMSS/`

#### 2. Uninstallation
- Uninstalls `TTS` package
- Verifies `import TTS` fails
- Archives TTS cache directories

#### 3. Installation
- Installs `qwen-tts>=1.0.0`
- Verifies `from qwen_tts import Qwen3TTSModel` works
- Saves new `pip freeze` output

#### 4. Configuration Update
- Updates `config/config.yaml`:
  - Model name → `Qwen/Qwen3-TTS-12Hz-1.7B-Base`
  - Sample rate → `12000`
  - Adds `dtype: "float32"`
  - Updates models path → `./data/qwen3_models`
- Creates `data/qwen3_models/` directory

#### 5. Verification
- Checks TTS is uninstalled
- Checks qwen-tts is installed
- Tests imports
- Runs basic tests

## Manual Migration

If you prefer to migrate manually:

### Step 1: Create Backup

```bash
# Create backup directory
mkdir -p backups/manual_migration_$(date +%Y%m%d)

# Backup files
cp -r config backups/manual_migration_$(date +%Y%m%d)/
cp requirements.txt backups/manual_migration_$(date +%Y%m%d)/
cp pyproject.toml backups/manual_migration_$(date +%Y%m%d)/
cp setup.py backups/manual_migration_$(date +%Y%m%d)/

# Backup voice profiles
cp data/*.json backups/manual_migration_$(date +%Y%m%d)/ 2>/dev/null || true

# Save pip state
pip freeze > backups/manual_migration_$(date +%Y%m%d)/pip_freeze_before.txt
```

### Step 2: Uninstall Coqui TTS

```bash
# Activate virtual environment
source venv/bin/activate

# Uninstall TTS
pip uninstall -y TTS

# Verify uninstallation
python -c "import TTS" 2>&1 | grep "No module named 'TTS'" && echo "✓ TTS uninstalled"
```

### Step 3: Clean Cache

```bash
# Archive TTS cache (don't delete, just move)
mkdir -p backups/manual_migration_$(date +%Y%m%d)/cache

# Move cache directories
mv ~/.local/share/tts backups/manual_migration_$(date +%Y%m%d)/cache/ 2>/dev/null || true
mv ~/.cache/tts backups/manual_migration_$(date +%Y%m%d)/cache/ 2>/dev/null || true
mv data/models/xtts-v2 backups/manual_migration_$(date +%Y%m%d)/cache/ 2>/dev/null || true
```

### Step 4: Install Qwen3-TTS

```bash
# Install qwen-tts
pip install qwen-tts>=1.0.0

# Verify installation
python -c "from qwen_tts import Qwen3TTSModel; print('✓ Qwen3-TTS installed')"

# Save new pip state
pip freeze > backups/manual_migration_$(date +%Y%m%d)/pip_freeze_after.txt
```

### Step 5: Update Configuration

Edit `config/config.yaml`:

```yaml
# Before:
model:
  name: "tts_models/multilingual/multi-dataset/xtts_v2"
  device: "auto"

audio:
  sample_rate: 22050

paths:
  models: "./data/models"

# After:
model:
  name: "Qwen/Qwen3-TTS-12Hz-1.7B-Base"
  device: "mps"  # or "cpu"
  dtype: "float32"  # Required for MPS

audio:
  sample_rate: 12000

paths:
  models: "./data/qwen3_models"
```

Create models directory:

```bash
mkdir -p data/qwen3_models
```

### Step 6: Verify Migration

```bash
# Run verification tests
pytest tests/test_qwen3_model_manager.py -v
pytest tests/test_qwen3_generator.py -v

# Test CLI
voice-clone info
```

## Post-Migration Steps

### 1. Update Voice Profiles

Old voice profiles need to be updated with `ref_text`:

```bash
# Option 1: Create new profile with ref_text
voice-clone prepare \
  --samples ./data/samples \
  --ref-text "Hola, esta es una muestra de mi voz para clonación." \
  --output ./data/voice_profile_qwen3.json \
  --name "my_voice"

# Option 2: Migrate existing profile
python scripts/migrate_voice_profile.py \
  --input ./data/old_profile.json \
  --output ./data/new_profile.json \
  --ref-text "Your reference text here"
```

### 2. Test Voice Generation

```bash
# Quick test
voice-clone test --profile ./data/voice_profile_qwen3.json

# Generate sample
voice-clone generate \
  --profile ./data/voice_profile_qwen3.json \
  --text "Esta es una prueba de la nueva voz con Qwen3-TTS." \
  --output ./test_qwen3.wav

# Play result (macOS)
afplay ./test_qwen3.wav
```

### 3. Update Your Workflow

Key changes to remember:

- **Sample rate**: Use 12000 Hz instead of 22050 Hz
- **Samples**: Only need 1-3 samples (not 6-10)
- **ref_text**: Required when creating voice profiles
- **Device**: Use "mps" for Apple Silicon, "cpu" otherwise
- **Dtype**: Must be "float32" for MPS

### 4. Regenerate Audio (Optional)

If you want to regenerate existing audio with the new model:

```bash
# Batch regenerate
voice-clone batch \
  --profile ./data/voice_profile_qwen3.json \
  --input ./data/scripts/my_script.txt \
  --output-dir ./data/outputs/regenerated_qwen3
```

## Rollback Procedure

If you need to rollback to Coqui TTS:

### Automated Rollback

```bash
# Set backup directory (from migration script output)
BACKUP_DIR="./backups/pre-qwen3-migration-YYYYMMDD_HHMMSS"

# 1. Restore configuration
cp -r $BACKUP_DIR/config/* ./config/

# 2. Restore dependency files
cp $BACKUP_DIR/requirements.txt .
cp $BACKUP_DIR/pyproject.toml .
cp $BACKUP_DIR/setup.py .

# 3. Reinstall old dependencies
source venv/bin/activate
pip uninstall -y qwen-tts
pip install -r $BACKUP_DIR/pip_freeze_before.txt
deactivate

# 4. Restore TTS cache (optional)
mv $BACKUP_DIR/cache/tts ~/.local/share/ 2>/dev/null || true

# 5. Verify rollback
source venv/bin/activate
python -c "from TTS.api import TTS; print('✓ Rollback successful')"
deactivate
```

### Manual Rollback

1. **Uninstall Qwen3-TTS**:
   ```bash
   pip uninstall -y qwen-tts
   ```

2. **Reinstall Coqui TTS**:
   ```bash
   pip install TTS>=0.22.0
   ```

3. **Restore configuration**:
   ```bash
   cp config_backup_YYYYMMDD/config.yaml config/
   ```

4. **Verify**:
   ```bash
   python -c "from TTS.api import TTS; print('✓ Rollback complete')"
   ```

## Troubleshooting

### Issue: "No module named 'TTS'" after migration

**Expected**: This is correct! TTS should not be importable after migration.

**If you need TTS**: Follow the [Rollback Procedure](#rollback-procedure).

### Issue: "Cannot import Qwen3TTSModel"

**Solution**:
```bash
# Reinstall qwen-tts
pip uninstall -y qwen-tts
pip install qwen-tts>=1.0.0

# Verify
python -c "from qwen_tts import Qwen3TTSModel"
```

### Issue: "MPS backend not available"

**Solution**:
```bash
# Check MPS availability
python -c "import torch; print(torch.backends.mps.is_available())"

# If False, use CPU instead
# Edit config/config.yaml:
# device: "cpu"
```

### Issue: Model download fails

**Solution**:
```bash
# Check internet connection
ping -c 3 huggingface.co

# Try manual download
python -c "from qwen_tts import Qwen3TTSModel; model = Qwen3TTSModel.from_pretrained('Qwen/Qwen3-TTS-12Hz-1.7B-Base')"

# Check disk space
df -h .
```

### Issue: Audio quality is poor

**Possible causes**:
1. **Old samples**: Re-record samples at 12000 Hz
2. **Missing ref_text**: Ensure voice profile has ref_text
3. **Wrong dtype**: Use float32 for MPS

**Solution**:
```bash
# Re-create voice profile with proper settings
voice-clone prepare \
  --samples ./data/samples \
  --ref-text "Clear reference text matching your samples" \
  --output ./data/new_profile.json
```

### Issue: "Out of memory" errors

**Solution**:
```bash
# Close other applications
# Reduce batch size in config.yaml:
# performance:
#   batch_size: 1

# Or use CPU instead of MPS
# device: "cpu"
```

### Issue: Tests failing after migration

**Expected**: Some tests may fail during migration. Key tests to check:

```bash
# These should pass:
pytest tests/test_qwen3_model_manager.py -v
pytest tests/test_qwen3_generator.py -v
pytest tests/test_config_qwen3.py -v

# These should fail (expected):
pytest tests/test_qwen3_migration_properties.py::TestCoquiTTSCompleteRemoval::test_tts_not_importable -v
# (Should fail with ImportError - this is correct!)
```

## FAQ

### Q: Can I keep both TTS and qwen-tts installed?

**A**: Not recommended. They may conflict. Choose one:
- For production: Use Qwen3-TTS
- For testing: Use separate virtual environments

### Q: Do I need to re-record my voice samples?

**A**: No, but you may want to:
- Old samples work fine (will be resampled to 12000 Hz)
- For best quality: Record new samples at 12000 Hz
- You only need 1-3 samples now (not 6-10)

### Q: What happens to my old voice profiles?

**A**: They're backed up but need updating:
- Add `ref_text` field
- Update `sample_rate` to 12000
- Use migration script or recreate profiles

### Q: Can I use CUDA with Qwen3-TTS?

**A**: Currently, Qwen3-TTS is optimized for:
- **MPS** (Apple Silicon) - Recommended
- **CPU** - Supported but slower
- **CUDA** - May work but not officially supported

### Q: How long does the first generation take?

**A**: First generation is slower due to model download:
- **Model download**: 5-10 minutes (~3.4GB)
- **Model loading**: 30-50 seconds
- **Generation**: 15-30 seconds per minute of audio

Subsequent generations are much faster (model stays loaded).

### Q: Is the migration reversible?

**A**: Yes! The migration script creates backups. See [Rollback Procedure](#rollback-procedure).

### Q: What if I have custom code using TTS.api?

**A**: You'll need to update your code:

```python
# Before (XTTS-v2):
from TTS.api import TTS
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

# After (Qwen3-TTS):
from qwen_tts import Qwen3TTSModel
model = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-Base")
```

See the [API documentation](docs/api.md) for details.

## Support

If you encounter issues not covered here:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review the backup location (printed by migration script)
3. Check logs in `./logs/` directory
4. Open an issue on GitHub with:
   - Error message
   - Output of `pip list`
   - Output of `voice-clone info`
   - Steps to reproduce

## Additional Resources

- [Qwen3-TTS Documentation](https://github.com/QwenLM/Qwen-Audio)
- [Project README](README.md)
- [Development Guide](docs/development.md)
- [API Documentation](docs/api.md)

---

**Migration completed successfully?** 🎉

Next steps:
1. Test voice generation
2. Update your workflows
3. Enjoy better voice cloning with Qwen3-TTS!
