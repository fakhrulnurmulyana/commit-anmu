# setup.py
# Project packaging configuration for anmu_buddy
# Allows installation and CLI execution using 'anmu_buddy' command
# To install in editable mode during development, run:
#       pip install -e .

from setuptools import setup, find_packages

setup(
    # Basic package metadata
    name="anmu_buddy",
    version="0.1.0",

    # Define where to find packages (using src/ layout)
    packages=find_packages(where="src"),
    package_dir={"": "src"},

    # External dependencies required by this package
    install_requires=["typer"],

    # Register CLI entry point for Typer app
    entry_points={
        "console_scripts": [
            "anmu_buddy=anmu_buddy.cli:app"
        ]
    },
)