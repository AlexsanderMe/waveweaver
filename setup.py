#!/usr/bin/env python3
"""
Setup script for WaveWeaver
Fallback para compatibilidade com sistemas que não têm build instalado
"""

from setuptools import setup, find_packages
from pathlib import Path

# Lê o README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Lê os requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = [
        line.strip() 
        for line in requirements_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="waveweaver",
    version="1.0.0",
    description="Audio stem separation application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="AlexsanderMe",
    author_email="alexsander.mei22@gmail.com",
    url="https://github.com/AlexsanderMe/waveweaver",
    project_urls={
        "Homepage": "https://github.com/AlexsanderMe/waveweaver",
        "Repository": "https://github.com/AlexsanderMe/waveweaver.git",
        "Issues": "https://github.com/AlexsanderMe/waveweaver/issues",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-qt>=4.0.0",
            "black>=22.0.0",
            "isort>=5.10.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ]
    },
    entry_points={
        "console_scripts": [
            "waveweaver=waveweaver.app:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio",
    ],
    keywords=["audio", "stem-separation", "demucs", "ai", "music"],
    license="MIT",
    include_package_data=True,
    zip_safe=False,
)