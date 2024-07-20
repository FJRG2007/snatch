from . import basics
import src.lib.colors as cl
from src.utils.basics import terminal
from contextlib import contextmanager
import os, re, sys, logging, itertools, multiprocessing

@contextmanager
def suppress_tensorflow_warnings():
    stderr = sys.stderr
    with open(os.devnull, "w") as devnull:
        sys.stderr = devnull
        try: yield
        finally: sys.stderr = stderr

def test_image(image_to_check, saveonfile):
    with suppress_tensorflow_warnings():
        for face_location in basics.face_locations(basics.load_image_file(image_to_check)):
            print(f"{cl.G} {os.path.basename(image_to_check)} {cl.w} {",".join(map(str, face_location))}")
            if saveonfile: 
                os.makedirs(f"output/image_analysis/detector/", exist_ok=True)
                with open(os.path.join("output/image_analysis/detector/", f"{os.path.basename(image_to_check)}.txt"), "w") as f:
                    f.write(",".join(map(str, face_location)))

def process_images_in_process_pool(images_to_check, number_of_cpus, model, upsample):
    if number_of_cpus == -1: processes = None
    else: processes = number_of_cpus
    # MacOS will crash due to a bug in libdispatch if you don"t use "forkserver".
    context = multiprocessing
    if "forkserver" in multiprocessing.get_all_start_methods(): context = multiprocessing.get_context("forkserver")
    context.Pool(processes=processes).starmap(test_image, zip(
        images_to_check,
        itertools.repeat(model),
        itertools.repeat(upsample),
    ))

def main(saveonfile):
    logging.basicConfig(level=logging.ERROR)
    # Multi-core processing only supported on Python 3.4 or greater.
    if (sys.version_info < (3, 4)): return terminal("w", "Multi-processing support requires Python 3.4 or greater. Falling back to single-threaded processing!")
    for filename in os.listdir("customs/image_analysis"):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")): test_image(os.path.join("customs/image_analysis", filename), saveonfile)