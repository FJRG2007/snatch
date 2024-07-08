import os, sys
import src.lib.colors as cl
from datetime import datetime
from src.utils.basics import terminal

from .extractors.snatch import snatch
from .extractors.exiftool import exiftool

def main(tool, saveonfile):
    tool = tool.lower()
    results = []
    output_folder = "output/extract_metadata"
    # Create output folder if it doesn't exist.
    if not os.path.exists(output_folder): os.makedirs(output_folder)
    for filename in os.listdir("customs/extract_metadata"):
        if filename == "WHAT_TO_PUT_HERE.txt": continue
        file_path = os.path.join("customs/extract_metadata", filename)
        if os.path.isfile(file_path):
            terminal("i", f"Extracting metadata from: {filename}")
            # Tools/Extractors.
            if (tool == "snatch"): result = snatch(filename)
            elif (tool == "exiftool"): result = exiftool(filename)
            else: return terminal("e", "Enter a valid extractor [snatch (default), exiftool].")
            if result:
                if result == "snatch_exception": return
                lines = result.splitlines()
                for line in lines:
                    print(f"{cl.des_space}{line}") # Print result in terminal.
                results.append(result)

    if saveonfile:
        output_filename = datetime.now().strftime("%Y%m%d_%H%M%S.txt")
        output_path = os.path.join(output_folder, output_filename)
        with open(output_path, "w", encoding="utf-8") as outfile:
            outfile.write("\n\n\n".join(results))
        terminal("s", f"Results saved to: {output_path}")
    terminal("s", f"Metadata extraction successfully completed.")