"""Package installer for funapis-response."""

from setuptools import setup, find_packages

# Read the README.md for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Core dependencies
install_requires = [
    # For datetime timezone handling
    "pytz>=2024.1",      
    # For JSON serialization & type validation
    "pydantic>=2.0.0",   
    # For better datetime handling
    "python-dateutil>=2.8.2",  
]

# Development and testing dependencies
dev_requires = [
    # Testing framework
    "pytest>=7.0.0",        
    # Code coverage
    "pytest-cov>=4.0.0",    
    # Code formatting
    "black>=22.0.0",        
    # Import sorting
    "isort>=5.0.0",         
    # Type checking
    "mypy>=1.0.0",          
    # Documentation generation
    "sphinx>=7.0.0",        
]

setup(
    # Basic package information
    name="funapis-response",
    version="0.1.1",
    author="B.J. Lin",
    author_email="bjlin@gmail.com",
    description="A standardized API response payload library for FUN-prefixed error codes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    # Project URLs
    url="https://github.com/bjlin888/funapis-response",
    project_urls={
        "Bug Tracker": "https://github.com/bjlin888/funapis-response/issues",
        "Documentation": "https://github.com/bjlin888/funapis-response#readme",
        "Source Code": "https://github.com/bjlin888/funapis-response",
    },
    
    # Package discovery
    packages=find_packages(exclude=["tests", "tests.*"]),
    
    # Package dependencies
    python_requires=">=3.9",
    install_requires=install_requires,
    extras_require={
        "dev": dev_requires,
    },
    
    # Package classifiers
    classifiers=[
        # Development status
        "Development Status :: 4 - Beta",
        
        # Intended audience
        "Intended Audience :: Developers",
        
        # License
        "License :: OSI Approved :: MIT License",
        
        # Operating system
        "Operating System :: OS Independent",
        
        # Python versions
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        
        # Environment
        "Environment :: Web Environment",
        
        # Framework
        "Framework :: FastAPI",
        "Framework :: Flask",
        
        # Topics
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
    ],
    
    # Package data
    package_data={
        "funapis_response": ["py.typed"],
    },
    
    # Entry points (if any CLI tools are provided)
    entry_points={
        "console_scripts": [
            # No CLI tools in this package yet
        ],
    },
)
