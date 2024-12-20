from setuptools import setup, find_packages

setup(
    name="fireflies-cli",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "python-dotenv",
        "fireflies-sdk",  # This will be our published SDK package
    ],
    entry_points={
        "console_scripts": [
            "ff=fireflies_cli.cli:cli",
        ],
    },
    author="David Schwartz",
    author_email="david.schwartz@devfactory.com",
    description="Command line interface for Fireflies.ai",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/trilogy-group/pocs",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
