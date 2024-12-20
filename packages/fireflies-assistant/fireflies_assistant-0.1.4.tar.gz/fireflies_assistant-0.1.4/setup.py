from setuptools import setup, find_packages

setup(
    name="fireflies-assistant",
    version="0.1.4",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "requests",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "ff=meet_joiner:cli",
        ],
    },
    author="Dan Schwartz",
    author_email="dan.schwartz@trilogy.com",
    description="A CLI tool for managing Fireflies.ai meetings and transcripts",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/trilogy-group/pocs/tree/main/fireflies-assistant",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
