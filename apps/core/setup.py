"""Setup configuration for tts-studio package."""

from pathlib import Path

from setuptools import find_packages, setup

# Read README for long description
readme_file = Path(__file__).parent.parent.parent / "README.md"
long_description = (
    readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""
)

setup(
    name="tts-studio",
    version="0.1.0-beta",
    description="Voice cloning and TTS library with hexagonal architecture for desktop applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Bryan Stevens Acosta",
    author_email="bryanstevensacosta@gmail.com",
    url="https://github.com/bryanstevensacosta/tts-studio",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10,<3.12",
    install_requires=[
        # TTS Engine
        "qwen-tts>=1.0.0",
        "torch>=2.0.0",
        "torchaudio>=2.0.0",
        # Audio Processing
        "soundfile>=0.12.0",
        "numpy>=1.24.0",
        "librosa>=0.10.0",
        "pydub>=0.25.0",
        "scipy>=1.10.0",
        # Configuration & Utilities
        "python-dotenv>=1.0.0",
        "PyYAML>=6.0",
        # DTOs and Data Validation
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "black>=23.0.0",
            "ruff>=0.1.0",
            "mypy>=1.0.0",
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pre-commit>=3.0.0",
            "hypothesis>=6.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="voice-cloning tts qwen3-tts speech-synthesis hexagonal-architecture desktop-app",
    license="MIT",
)
