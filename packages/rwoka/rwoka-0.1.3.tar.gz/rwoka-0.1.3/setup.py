from setuptools import setup, find_packages

# Dependencies
install_requires = [
    "requests",    
]

setup(
    name="rwoka",
    version="0.1.3",
    author="marry queen",
    author_email="marryqueen2024@hotmail.com",
    description="Simplified HTTP requests and GitHub package installer.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/marryqueen2024/intranetflow",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    keywords="intranetflow https ",
    python_requires=">=3.9",
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "rwoka=intranetflow.netcore:main",
        ],
    },
    zip_safe=False,
)
