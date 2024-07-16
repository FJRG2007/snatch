import random, string as st
from .generator import generate_wordlist_from_profile
from src.utils.basics import quest, terminal, getPositive

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

def main():
    terminal("info", f"""Welcome, then I will ask you some questions to generate possible passwords.
* Insert the information about the victim to make a dictionary.
* If you don't know all the info, just hit enter when asked!""")
    profile = {}
    # Victim's name/target.
    profile["name"] = quest("First Name", newline=True, lowercase=True)
    while len(profile["name"]) == 0:
        terminal("e", "You must enter a name at least!")
        profile["name"] = quest("First Name", newline=True, lowercase=True)
    profile["surname"] = quest("Surname", lowercase=True)
    profile["nick"] = quest("Nickname", lowercase=True)
    profile["birthdate"] = quest("Birthdate (MMDDYYYY)", lowercase=True)
    while len(profile["birthdate"]) != 0 and len(profile["birthdate"]) != 8:
        terminal("e", "You must enter 8 digits for birthday!")
        profile["birthdate"] = quest("Birthdate (MMDDYYYY)", newline=True, lowercase=True)
    print("\r\n")
    profile["wife"] = quest("Partners) name", lowercase=True)
    profile["wifen"] = quest("Partners) nickname", lowercase=True)
    profile["wifeb"] = quest("Partners) birthdate (DDMMYYYY)", lowercase=True)
    while len(profile["wifeb"]) != 0 and len(profile["wifeb"]) != 8:
        terminal("e", "You must enter 8 digits for birthday!")
        profile["wifeb"] = quest("Partners birthdate (DDMMYYYY)", newline=True, lowercase=True)
    print("\r\n")
    profile["kid"] = quest("Child's name", lowercase=True)
    profile["kidn"] = quest("Child's nickname", lowercase=True)
    profile["kidb"] = quest("Child's birthdate (DDMMYYYY)", lowercase=True)
    while len(profile["kidb"]) != 0 and len(profile["kidb"]) != 8:
        terminal("e", "You must enter 8 digits for birthday!")
        profile["kidb"] = quest("Child's birthdate (DDMMYYYY)", newline=True, lowercase=True)
    print("\r\n")
    # Victim's pet's name.
    profile["pet"] = quest("Pet's name", lowercase=True)
    # Name where the victim works/has worked.
    profile["company"] = quest("Company name", lowercase=True)
    print("\r\n")
    # Customized words.
    if getPositive(quest("Do you want to add some key words about the victim? Y/[N]"), default=False): profile["words"] = quest("Please enter the words, separated by comma. [i.e. hacker,juice,black], spaces will be removed").replace(" ", "").split(",")
    else: profile["words"] = [""]

    profile["spechars1"] = getPositive(quest("Do you want to add special chars at the end of words? Y/[N]"), default=False)

    profile["randnum"] = getPositive(quest("Do you want to add some random numbers at the end of words? Y/[N]"), default=False)
   
    profile["leetmode"] = getPositive(quest("Leet mode? (i.e. leet = 1337) Y/[N]", lowercase=True), default=False)

    generate_wordlist_from_profile(profile)