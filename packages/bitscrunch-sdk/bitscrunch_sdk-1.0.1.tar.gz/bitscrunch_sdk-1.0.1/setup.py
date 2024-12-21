from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bitscrunch-sdk",  
    version="1.0.1", 
    author="Ashok Varadharajan",
    author_email="ashok@bitscrunch.com",
    description="Python SDK for interacting with the BitsCrunch API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://docs.bitscrunch.com",
    project_urls={
        "Documentation": "https://github.com/bitscrunch-protocol/bitscrunch-sdk",
        "Bug Tracker": "https://github.com/bitscrunch-protocol/bitscrunch-sdk/issues",
        "Source Code": "https://github.com/bitscrunch-protocol/bitscrunch-sdk",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),  
    python_requires=">=3.8",
    install_requires=[
        "httpx>=0.24.1", 
        "pycryptodome>=3.17",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=0.991",
        ],
    },
    include_package_data=True,
    entry_points={},
    license="Apache License 2.0",
)
