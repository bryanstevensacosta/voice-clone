"""Setup configuration for voice-clone-cli package."""
from setuptools import find_packages, setup

setup(
    name="voice-clone-cli",
    version="0.2.0",
    description="Personal voice cloning CLI tool using Qwen3-TTS",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Bryan Stevens Acosta",
    author_email="bryanstevensacosta@gmail.com",
    url="https://github.com/yourusername/voice-clone-cli",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10,<3.12",
    install_requires=[
        "qwen-tts>=1.0.0",
        "torch>=2.0.0",
        "torchaudio>=2.0.0",
        "soundfile>=0.12.0",
        "numpy>=1.24.0",
        "librosa>=0.10.0",
        "pydub>=0.25.0",
        "scipy>=1.10.0",
        "click>=8.1.0",
        "rich>=13.0.0",
        "tqdm>=4.65.0",
        "python-dotenv>=1.0.0",
        "PyYAML>=6.0",
        "matplotlib>=3.5.0",
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
    entry_points={
        "console_scripts": [
            "voice-clone=cli.cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="voice-cloning tts qwen3-tts cli speech-synthesis",
    license="MIT",
)
