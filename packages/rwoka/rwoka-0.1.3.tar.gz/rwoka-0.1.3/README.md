# IntraNetFlow

**IntraNetFlow** is a Python package that simplifies HTTP requests, multi-threaded URL handling, and package installation from GitHub sources. It is designed to be efficient, easy-to-use, and integrate seamlessly into your projects. 

This package is particularly useful for automating HTTP requests (GET and POST) and installing Python packages directly from GitHub releases.

## Features

- **HTTP Request Handling**:
  - Perform GET and POST requests easily.
  - Support for single and multiple URLs with threading for enhanced performance.
  
- **GitHub Package Installation**:
  - Install Python packages directly from GitHub using a predefined or custom source URL.
  - URL validation ensures security and prevents malicious downloads.

- **Internet Connection Check**:
  - Check for active internet connectivity before initiating downloads or requests.
  
# import module

```
from IntraNetFlow import IntraNetFlow, PackageManager

```

# Perform HTTP GET Requests

```
response = IntraNetFlow.get("https://example.com")
print(response.text)

```
# multiple url
```
urls = ["https://example.com", "https://example.org"]
responses = IntraNetFlow.get(urls)
for response in responses:
    print(f"{response.url}: {response.status_code}")

```
# Perform HTTP POST Requests

```
response = IntraNetFlow.post("https://example.com/api", data={"key": "value"})
print(response.text)
```
# Install a Package from GitHub

Default GitHub Source
By default, the package installs from a predefined GitHub URL:

```
pm = PackageManager()
pm.install()
```
# Installation

You can install this package from PyPI:

```bash
pip install rwoka
```