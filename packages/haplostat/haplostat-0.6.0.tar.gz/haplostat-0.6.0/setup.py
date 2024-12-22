from setuptools import setup, find_packages

setup(
    name="haplostat",  # Your package name
    version="0.6.0",  # Increment version as needed
    description="A package for handling HLA-related tasks with Selenium WebDriver integration",
    long_description=open("README.md", "r", encoding="utf-8").read(),  # Ensure correct encoding
    long_description_content_type="text/markdown",
    author="Jesse",
    author_email="woopeejesse@gmail.com",
    url="https://github.com/jesse141245/haplostat",  # Replace with your repo or website
    packages=find_packages(),  # Automatically find all packages in your project
    install_requires=[
        "flask>=2.0.0",  # Flask for API
        "selenium>=4.0.0",  # Selenium for WebDriver automation
        "beautifulsoup4>=4.10.0",  # Correct dependency name for BeautifulSoup
        "requests>=2.26.0",  # Requests for HTTP handling
        "webdriver-manager>=3.8.5"  # WebDriver Manager to simplify driver setup
    ],
    python_requires=">=3.6",  # Specify the supported Python version
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    include_package_data=True,  # Include additional files like WebDriver binaries if needed
    entry_points={
        "console_scripts": [
            "haplo-cli=haplo.main:run_convert_hla",  # CLI entry point
        ]
    },
    package_data={
        "haplo": [
            "drivers/*",  # Include platform-specific WebDriver binaries if required
        ],
    },
)
