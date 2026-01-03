"""
ARKADAŠ - The King's Chamber
==============================

Organic ⚭ Digital Synchronization System
Sacred Geometry at 1/3 Pyramid Height
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="arkadas",
    version="0.1.0",
    author="Nexus Infinity",
    description="The King's Chamber: Organic ⚭ Digital Synchronization at 1/3 pyramid height",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nexus-infinity/arkadas",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: System :: Distributed Computing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.11",
    install_requires=[
        "PyYAML>=6.0.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
            "mypy>=1.5.0",
        ],
    },
    include_package_data=True,
    keywords="sacred-geometry pyramid synchronization collective-intelligence sensor-fusion",
    project_urls={
        "Documentation": "https://github.com/nexus-infinity/arkadas/tree/main/docs",
        "Source": "https://github.com/nexus-infinity/arkadas",
        "Bug Reports": "https://github.com/nexus-infinity/arkadas/issues",
    },
)
