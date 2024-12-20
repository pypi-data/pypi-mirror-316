"""
NetCore - A Python module for HTTP requests and GitHub package installation.

Features:
- Perform GET and POST HTTP requests with threading support.
- Install Python packages directly from GitHub sources securely.
- Check for internet connectivity before executing network operations.

Author: [Your Name]
License: MIT
Version: 0.1.0
"""

# Import everything from netcore.py
from .netcore import IntraNetFlow, PackageInstaller, PackageManager, is_connected

# Metadata
__author__ = "[Your Name]"
__license__ = "MIT"
__version__ = "0.1.0"

# Public API
__all__ = [
    "IntraNetFlow",
    "PackageInstaller",
    "PackageManager",
    "is_connected",
]
