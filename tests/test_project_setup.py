"""Unit tests for project setup and structure.

Tests that all required directories exist and dependencies are properly configured.
Validates: Requirements 8.1
"""
from pathlib import Path


def test_required_directories_exist() -> None:
    """Test that all required directories exist."""
    required_dirs = [
        "src/voice_clone",
        "src/voice_clone/audio",
        "src/voice_clone/model",
        "src/voice_clone/batch",
        "src/voice_clone/utils",
        "config",
        "data",
        "data/samples",
        "data/outputs",
        "data/models",
        "tests",
    ]

    for dir_path in required_dirs:
        path = Path(dir_path)
        assert path.exists(), f"Required directory does not exist: {dir_path}"
        assert path.is_dir(), f"Path exists but is not a directory: {dir_path}"


def test_package_init_files_exist() -> None:
    """Test that all package __init__.py files exist."""
    required_init_files = [
        "src/voice_clone/__init__.py",
        "src/voice_clone/audio/__init__.py",
        "src/voice_clone/model/__init__.py",
        "src/voice_clone/batch/__init__.py",
        "src/voice_clone/utils/__init__.py",
        "tests/__init__.py",
    ]

    for init_file in required_init_files:
        path = Path(init_file)
        assert path.exists(), f"Required __init__.py file does not exist: {init_file}"
        assert path.is_file(), f"Path exists but is not a file: {init_file}"


def test_config_files_exist() -> None:
    """Test that configuration files exist."""
    required_config_files = [
        "config/default.yaml",
        "setup.py",
        "requirements.txt",
        "pyproject.toml",
        ".gitignore",
    ]

    for config_file in required_config_files:
        path = Path(config_file)
        assert path.exists(), f"Required config file does not exist: {config_file}"
        assert path.is_file(), f"Path exists but is not a file: {config_file}"


def test_default_config_has_required_sections() -> None:
    """Test that default.yaml contains all required configuration sections."""
    import yaml  # type: ignore[import-untyped]

    config_path = Path("config/default.yaml")
    with open(config_path) as f:
        config = yaml.safe_load(f)

    required_sections = [
        "model",
        "audio",
        "paths",
        "generation",
        "performance",
        "logging",
    ]

    for section in required_sections:
        assert section in config, f"Required config section missing: {section}"

    # Verify key settings in each section
    assert "name" in config["model"]
    assert "device" in config["model"]

    assert "sample_rate" in config["audio"]
    assert config["audio"]["sample_rate"] == 22050, "Sample rate should be 22050 Hz"

    assert "samples" in config["paths"]
    assert "outputs" in config["paths"]
    assert "models" in config["paths"]

    assert "language" in config["generation"]
    assert "temperature" in config["generation"]
    assert "max_length" in config["generation"]


def test_gitignore_excludes_data_directories() -> None:
    """Test that .gitignore properly excludes data directories."""
    gitignore_path = Path(".gitignore")

    with open(gitignore_path) as f:
        gitignore_content = f.read()

    required_ignores = [
        "data/samples/",
        "data/outputs/",
        "data/models/",
        "config/config.yaml",
    ]

    for ignore_pattern in required_ignores:
        assert (
            ignore_pattern in gitignore_content
        ), f"Required ignore pattern not in .gitignore: {ignore_pattern}"


def test_setup_py_has_required_fields() -> None:
    """Test that setup.py contains all required fields."""
    setup_path = Path("setup.py")

    with open(setup_path) as f:
        setup_content = f.read()

    required_fields = [
        "name=",
        "version=",
        "description=",
        "packages=",
        "install_requires=",
        "entry_points=",
    ]

    for field in required_fields:
        assert field in setup_content, f"Required field not in setup.py: {field}"

    # Verify entry point
    assert (
        "voice-clone=voice_clone.cli:cli" in setup_content
    ), "CLI entry point not properly configured"


def test_requirements_txt_has_core_dependencies() -> None:
    """Test that requirements.txt contains all core dependencies."""
    requirements_path = Path("requirements.txt")

    with open(requirements_path) as f:
        requirements_content = f.read()

    core_dependencies = [
        "TTS",
        "torch",
        "torchaudio",
        "soundfile",
        "numpy",
        "librosa",
        "click",
        "rich",
        "PyYAML",
    ]

    for dependency in core_dependencies:
        assert (
            dependency in requirements_content
        ), f"Required dependency not in requirements.txt: {dependency}"


def test_package_is_importable() -> None:
    """Test that the voice_clone package can be imported."""
    try:
        import voice_clone  # noqa: F401

        # Package exists and is importable
        assert True
    except ImportError as e:
        raise AssertionError(f"Cannot import voice_clone package: {e}") from e


def test_cli_module_exists() -> None:
    """Test that the CLI module exists and can be imported."""
    try:
        from voice_clone import cli

        assert hasattr(cli, "cli"), "CLI entry point function not found"
    except ImportError as e:
        raise AssertionError(f"Cannot import CLI module: {e}") from e


def test_pyproject_toml_configuration() -> None:
    """Test that pyproject.toml is properly configured."""
    import tomli

    pyproject_path = Path("pyproject.toml")

    with open(pyproject_path, "rb") as f:
        pyproject = tomli.load(f)

    # Check project metadata
    assert "project" in pyproject
    assert pyproject["project"]["name"] == "voice-clone-cli"
    assert "version" in pyproject["project"]

    # Check scripts entry point
    assert "project" in pyproject
    assert "scripts" in pyproject["project"]
    assert "voice-clone" in pyproject["project"]["scripts"]

    # Check tool configurations
    assert "tool" in pyproject
    assert "pytest" in pyproject["tool"]
    assert "coverage" in pyproject["tool"]
