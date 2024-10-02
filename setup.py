from pathlib import Path
from setuptools import setup, find_packages

def find_data_files(directory):
    # Finds all files in the directory and subdirectories.
    data_files = []
    for path in Path(directory).glob('**/*.json'):
        data_files.append(str(path.relative_to(directory)))
    return data_files

setup(
    name="snatch",
    version="0.1.0",
    packages=find_packages(),
    keywords=["artificial intelligence", "osint", "reconnaissance", "information gathering"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "snatch = src.cli:main"
        ]
    },
    package_data={
        "": find_data_files("src")
    }
)