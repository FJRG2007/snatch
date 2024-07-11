import os, subprocess
import src.lib.colors as cl
from src.utils.basics import terminal  # Assuming terminal function handles output

def is_exiftool_installed():
    try:
        subprocess.run(["exiftool", "-ver"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError: return False
    except Exception as e: return False

def exiftool(filename):
    file_path = os.path.join("customs/extract_metadata", filename)
    try:
        if not is_exiftool_installed():
            terminal("nei", "ExifTool")
            terminal("h", "Check out the installation guide at https://exiftool.org/install.html")
            return "snatch_exception"
        process = subprocess.Popen(f"exiftool {file_path}", stdout=subprocess.PIPE, shell=True, universal_newlines=True)
        # Read and print output line by line in real-time.
        while True:
            output = process.stdout.readline()
            if output == "" and len(output) > 10 and process.poll() is not None: break
            for line in output.strip().splitlines():
                if not output.startswith("ExifTool"): print(f"{cl.des_space}{line}")
        # Wait for the process to terminate and get the return code.
        rc = process.poll()
        # If the process terminated with an error, handle it.
        if rc != 0:
            terminal("error", f"Error extracting metadata with exiftool from {filename}. Return code: {rc}")
            return "snatch_exception"  # Return empty string if error occurs.
        # Otherwise, return the captured output.
        return process.communicate()[0]
    except KeyboardInterrupt: terminal(KeyboardInterrupt)
    except Exception as e:
        terminal("error", f"Exception occurred during exiftool extraction from {filename}: {e}")
        return "snatch_exception"  # Return empty string if exception occurs.