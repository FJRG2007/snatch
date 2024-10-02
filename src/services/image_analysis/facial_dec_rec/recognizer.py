
from . import basics
from src.utils.basics import terminal
import os, re, sys, numpy as np, PIL.Image, itertools, multiprocessing
def scan_known_people(known_people_folder):
    known_names = []
    known_face_encodings = []
    for file in [os.path.join(known_people_folder, f) for f in os.listdir(known_people_folder) if re.match(r".*\.(jpg|jpeg|png)", f, flags=re.I)]:
        encodings = basics.face_encodings(basics.load_image_file(file))
        if len(encodings) > 1: terminal("w", "More than one face found in {}. Only considering the first face.".format(file))
        if len(encodings) == 0: terminal("w", "No faces found in {}. Ignoring file.".format(file))
        else:
            known_names.append(os.path.splitext(os.path.basename(file))[0])
            known_face_encodings.append(encodings[0])
    return known_names, known_face_encodings

def print_result(filename, name, distance, show_distance=False) -> None:
    if show_distance: print("{},{},{}".format(filename, name, distance))
    else: print("{},{}".format(filename, name))

def test_image(image_to_check, known_names, known_face_encodings, tolerance=0.6, show_distance=False):
    unknown_image = basics.load_image_file(image_to_check)
    # Scale down image if it"s giant so things run a little faster.
    if max(unknown_image.shape) > 1600:
        pil_img = PIL.Image.fromarray(unknown_image)
        pil_img.thumbnail((1600, 1600), PIL.Image.LANCZOS)
    unknown_encodings = basics.face_encodings(np.array(pil_img))
    for unknown_encoding in unknown_encodings:
        distances = basics.face_distance(known_face_encodings, unknown_encoding)
        result = list(distances <= tolerance)
        if True in result: [print_result(image_to_check, name, distance, show_distance) for is_match, name, distance in zip(result, known_names, distances) if is_match]
        else: print_result(image_to_check, "unknown_person", None, show_distance)
    if not unknown_encodings: print_result(image_to_check, "no_persons_found", None, show_distance)

def process_images_in_process_pool(images_to_check, known_names, known_face_encodings, number_of_cpus, tolerance, show_distance):
    # MacOS will crash due to a bug in libdispatch if you don"t use "forkserver".
    (multiprocessing.get_context("forkserver") if "forkserver" in multiprocessing.get_all_start_methods() else multiprocessing).Pool(processes=None if number_of_cpus == -1 else number_of_cpus).starmap(test_image, zip(
        images_to_check,
        itertools.repeat(known_names),
        itertools.repeat(known_face_encodings),
        itertools.repeat(tolerance),
        itertools.repeat(show_distance)
    ))

def main(known_people_folder, image_to_check, cpus, tolerance, show_distance):
    # Multi-core processing only supported on Python 3.4 or greater.
    if (sys.version_info < (3, 4)): return terminal("w", "Multi-processing support requires Python 3.4 or greater. Falling back to single-threaded processing!")
    known_names, known_face_encodings = scan_known_people(known_people_folder)
    test_image(image_to_check, known_names, known_face_encodings, tolerance, show_distance)