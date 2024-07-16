import src.lib.colors as cl
from datetime import datetime
import os, random, string as st
from src.utils.basics import terminal

equivalences = [
    ("d", "Only digits"),
    ("l", "Only lower-case letters"),
    ("u", "Only upper-case letters"),
    ("p", "Only punctuation characters"),
    ("a", "All characters")
]

def get_equivalent(key):
    for k, v in equivalences:
        if k == key: return v
    return None

def generate_password(pwd_characters, length):
    characters = []
    if "d" in pwd_characters: characters += st.digits
    if "l" in pwd_characters: characters += st.ascii_lowercase
    if "u" in pwd_characters: characters += st.ascii_uppercase
    if "p" in pwd_characters: characters += st.punctuation
    if "a" in pwd_characters: characters += (st.digits + st.ascii_lowercase + st.ascii_uppercase + st.punctuation)
    random.shuffle(characters)
    return "".join(characters[:length])

def main(characters, length=20, iterations=50):
    target= ""
    # Add Banner.
    print("-" * 50)
    print(f"Scanning Target: {target}")
    print(f"Characters: {get_equivalent(characters)}") # Change coming soon.
    print(f"Scanning started at: {str(datetime.now())}")
    print(f"Number of iterations: {iterations}")
    print("-" * 50 + f"\n{cl.w}")
    pwd_list = []
    for i in range(iterations):
       pwd_list.append(generate_password("a", length))
    pwd_list = set(pwd_list)
    print(pwd_list, sep="\n")
    # with open (f"output/password_generator/{target}.txt") as file:
    #     for pwd in pwd_list:
    #         file.write(f"{pwd}\n")