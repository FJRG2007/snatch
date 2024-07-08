import platform
import os
import shutil
import zipfile
import subprocess
from ..basics import terminal

def install_exiftool():
    # Detect the operating system.
    system = platform.system()
    if system == "Windows":
        terminal("s", "Windows detected.")
        # Download ExifTool zip file.
        os.system("curl -o ExifTool.zip https://exiftool.org/ExifTool-12.87.zip")
        # Unzip ExifTool.zip.
        try:
            with zipfile.ZipFile("ExifTool.zip", 'r') as zip_ref:
                zip_ref.extractall("ExifTool")
                terminal("s", "ExifTool extracted successfully.")
        except zipfile.BadZipFile: terminal("e", "ExifTool.zip is not a valid zip file.")
        # Rename the executable file and move it to C:/Windows.
        try:
            shutil.move("ExifTool/exiftool(-k).exe", "C:/Windows/exiftool.exe")
            terminal("s", "ExifTool executable renamed and moved to C:/Windows.")
        except FileNotFoundError: terminal("e", "ExifTool executable not found.")
    
    elif system == "Linux" or system == "Darwin":
        terminal("s", f"{system} detected.")
        try:
            # Install ExifTool using the appropriate package manager
            subprocess.run(["sudo", "apt-get", "install", "-y", "exiftool"] if system == "Linux" else ["brew", "install", "exiftool"], check=True)
            terminal("s", "ExifTool installed successfully.")
        except subprocess.CalledProcessError as e: terminal("e", f"Error installing ExifTool: {e}")
    
    else: terminal("e", f"Unsupported system: {system}. Cannot install ExifTool automatically.")