from setuptools import setup, find_packages

setup(
    name="everythingjs",  # Name of the module
    version="0.1.0",  # Version of the module
    packages=find_packages(),  # Automatically find packages
    install_requires=[  # List of dependencies
        'beautifulsoup4',  # HTML parsing
        'requests',         # HTTP requests
    ],
    entry_points={
        'console_scripts': [
             'everythingjs=everythingjs.app:main',  # CLI entry point
        ],
    },
)
