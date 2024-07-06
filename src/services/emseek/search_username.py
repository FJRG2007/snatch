import os, subprocess
from ...utils.basics import terminal

def search_username(username, saveonfile):
    try:
        try: subprocess.check_output("pip install sherlock-project", shell=True, text=True)
        except subprocess.CalledProcessError: return terminal("nmi", "Sherlock")
        process = subprocess.Popen(f"sherlock {username} --nsfw", shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        # Open file for writing if saveonfile is True.
        if saveonfile:
            os.makedirs("output/emseek", exist_ok=True)
            file = open(f"output/emseek/{username}_results.txt", "w")
        while True:
            output = process.stdout.readline().strip()
            if output.startswith("[") and output[2] == "]": output = output[4:]
            if output == "" and len(output) > 10 and process.poll() is not None: break
            if output.startswith("Checking username "): terminal("i", f"{output}\nThis may take a few minutes...")
            elif output.startswith("Search completed with "): terminal("s", f"{output}."); break
            elif len(output) > 10: 
                print(output)
                if saveonfile: file.write(output + "\n")
        return process.poll()
    except KeyboardInterrupt: terminal(KeyboardInterrupt)
    except Exception as e: terminal("e", f"Error obtaining Sherlock data: {e}")