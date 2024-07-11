from setuptools import setup, find_packages

setup(
    name="snatch",
    version="0.1.0",
    packages=find_packages(),
    keywords=["artificial intelligence", "osint", "reconnaissance", "information gathering"],
    include_package_data=True,
    entry_points = {
        "console_scripts": [
            "snatch = src.cli:main",
        ],
    },
)