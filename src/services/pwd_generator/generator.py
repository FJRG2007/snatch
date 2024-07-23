import os, string as st
import src.lib.colors as cl
from src.utils.basics import cls, quest, terminal, getPositive

# For concatenations...
def concats(seq, start, stop):
    for mystr in seq:
        for num in range(start, stop):
            yield mystr + str(num)

# For sorting and making combinations...
def komb(seq, start, special=""):
    for mystr in seq:
        for mystr1 in start:
            yield mystr + special + mystr1

def print_to_file(filename, unique_list_finished):
    print(unique_list_finished)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    f = open(filename, "w")
    unique_list_finished.sort()
    f.write(os.linesep.join(unique_list_finished))
    f.close()
    f = open(filename, "r")
    lines = 0
    for line in f:
        lines += 1
    f.close()
    print(f"{cl.b}Saving dictionary to \033[1;31m{filename}\033[1;m, counting \033[1;31m{str(lines)} words.\033[1;m")

# Generates a wordlist from a given profile.
def generate_wordlist_from_profile(profile):
    years = ["1990", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]
    numfrom = 0
    numto = 100

    profile["spechars"] = []

    if profile["spechars1"]:
        for spec1 in st.punctuation:
            profile["spechars"].append(spec1)
            for spec2 in st.punctuation:
                profile["spechars"].append(spec1 + spec2)
                for spec3 in st.punctuation:
                    profile["spechars"].append(spec1 + spec2 + spec3)

    terminal("i", "Now making a dictionary...")

    # Birthdays first.
    birthdate_yy = profile["birthdate"][-2:]
    birthdate_yyy = profile["birthdate"][-3:]
    birthdate_yyyy = profile["birthdate"][-4:]
    birthdate_xd = profile["birthdate"][1:2]
    birthdate_xm = profile["birthdate"][3:4]
    birthdate_dd = profile["birthdate"][:2]
    birthdate_mm = profile["birthdate"][2:4]

    wifeb_yy = profile["wifeb"][-2:]
    wifeb_yyy = profile["wifeb"][-3:]
    wifeb_yyyy = profile["wifeb"][-4:]
    wifeb_xd = profile["wifeb"][1:2]
    wifeb_xm = profile["wifeb"][3:4]
    wifeb_dd = profile["wifeb"][:2]
    wifeb_mm = profile["wifeb"][2:4]

    kidb_yy = profile["kidb"][-2:]
    kidb_yyy = profile["kidb"][-3:]
    kidb_yyyy = profile["kidb"][-4:]
    kidb_xd = profile["kidb"][1:2]
    kidb_xm = profile["kidb"][3:4]
    kidb_dd = profile["kidb"][:2]
    kidb_mm = profile["kidb"][2:4]

    # Convert first letters to uppercase...

    nameup = profile["name"].title()
    surnameup = profile["surname"].title()
    nickup = profile["nick"].title()
    wifeup = profile["wife"].title()
    wifenup = profile["wifen"].title()
    kidup = profile["kid"].title()
    kidnup = profile["kidn"].title()
    petup = profile["pet"].title()
    companyup = profile["company"].title()

    wordsup = []
    wordsup = list(map(str.title, profile["words"]))

    word = profile["words"] + wordsup

    # Reverse a name.

    rev_name = profile["name"][::-1]
    rev_nameup = nameup[::-1]
    rev_nick = profile["nick"][::-1]
    rev_nickup = nickup[::-1]
    rev_wife = profile["wife"][::-1]
    rev_wifeup = wifeup[::-1]
    rev_kid = profile["kid"][::-1]
    rev_kidup = kidup[::-1]

    reverse = [
        rev_name,
        rev_nameup,
        rev_nick,
        rev_nickup,
        rev_wife,
        rev_wifeup,
        rev_kid,
        rev_kidup,
    ]
    rev_n = [rev_name, rev_nameup, rev_nick, rev_nickup]
    rev_w = [rev_wife, rev_wifeup]
    rev_k = [rev_kid, rev_kidup]

    # Birthdays combinations.
    bds = [
        birthdate_yy,
        birthdate_yyy,
        birthdate_yyyy,
        birthdate_xd,
        birthdate_xm,
        birthdate_dd,
        birthdate_mm,
    ]

    bdss = []

    for bds1 in bds:
        bdss.append(bds1)
        for bds2 in bds:
            if bds.index(bds1) != bds.index(bds2):
                bdss.append(bds1 + bds2)
                for bds3 in bds:
                    if (bds.index(bds1) != bds.index(bds2) and bds.index(bds2) != bds.index(bds3) and bds.index(bds1) != bds.index(bds3)): bdss.append(bds1 + bds2 + bds3)
                # For a woman...
    wbds = [wifeb_yy, wifeb_yyy, wifeb_yyyy, wifeb_xd, wifeb_xm, wifeb_dd, wifeb_mm]

    wbdss = []

    for wbds1 in wbds:
        wbdss.append(wbds1)
        for wbds2 in wbds:
            if wbds.index(wbds1) != wbds.index(wbds2):
                wbdss.append(wbds1 + wbds2)
                for wbds3 in wbds:
                    if (wbds.index(wbds1) != wbds.index(wbds2) and wbds.index(wbds2) != wbds.index(wbds3) and wbds.index(wbds1) != wbds.index(wbds3)): wbdss.append(wbds1 + wbds2 + wbds3)

                # And a child...
    kbds = [kidb_yy, kidb_yyy, kidb_yyyy, kidb_xd, kidb_xm, kidb_dd, kidb_mm]

    kbdss = []

    for kbds1 in kbds:
        kbdss.append(kbds1)
        for kbds2 in kbds:
            if kbds.index(kbds1) != kbds.index(kbds2):
                kbdss.append(kbds1 + kbds2)
                for kbds3 in kbds:
                    if (kbds.index(kbds1) != kbds.index(kbds2) and kbds.index(kbds2) != kbds.index(kbds3) and kbds.index(kbds1) != kbds.index(kbds3)): kbdss.append(kbds1 + kbds2 + kbds3)

                # String combinations....
    kombinaac = [profile["pet"], petup, profile["company"], companyup]

    kombina = [
        profile["name"],
        profile["surname"],
        profile["nick"],
        nameup,
        surnameup,
        nickup,
    ]

    kombinaw = [
        profile["wife"],
        profile["wifen"],
        wifeup,
        wifenup,
        profile["surname"],
        surnameup,
    ]

    kombinak = [
        profile["kid"],
        profile["kidn"],
        kidup,
        kidnup,
        profile["surname"],
        surnameup,
    ]

    kombinaa = []
    for kombina1 in kombina:
        kombinaa.append(kombina1)
        for kombina2 in kombina:
            if kombina.index(kombina1) != kombina.index(kombina2) and kombina.index(kombina1.title()) != kombina.index(kombina2.title()): kombinaa.append(kombina1 + kombina2)

    kombinaaw = []
    for kombina1 in kombinaw:
        kombinaaw.append(kombina1)
        for kombina2 in kombinaw:
            if kombinaw.index(kombina1) != kombinaw.index(kombina2) and kombinaw.index(kombina1.title()) != kombinaw.index(kombina2.title()): kombinaaw.append(kombina1 + kombina2)

    kombinaak = []
    for kombina1 in kombinak:
        kombinaak.append(kombina1)
        for kombina2 in kombinak:
            if kombinak.index(kombina1) != kombinak.index(kombina2) and kombinak.index(kombina1.title()) != kombinak.index(kombina2.title()): kombinaak.append(kombina1 + kombina2)

    kombi = {}
    kombi[1] = list(komb(kombinaa, bdss))
    kombi[1] += list(komb(kombinaa, bdss, "_"))
    kombi[2] = list(komb(kombinaaw, wbdss))
    kombi[2] += list(komb(kombinaaw, wbdss, "_"))
    kombi[3] = list(komb(kombinaak, kbdss))
    kombi[3] += list(komb(kombinaak, kbdss, "_"))
    kombi[4] = list(komb(kombinaa, years))
    kombi[4] += list(komb(kombinaa, years, "_"))
    kombi[5] = list(komb(kombinaac, years))
    kombi[5] += list(komb(kombinaac, years, "_"))
    kombi[6] = list(komb(kombinaaw, years))
    kombi[6] += list(komb(kombinaaw, years, "_"))
    kombi[7] = list(komb(kombinaak, years))
    kombi[7] += list(komb(kombinaak, years, "_"))
    kombi[8] = list(komb(word, bdss))
    kombi[8] += list(komb(word, bdss, "_"))
    kombi[9] = list(komb(word, wbdss))
    kombi[9] += list(komb(word, wbdss, "_"))
    kombi[10] = list(komb(word, kbdss))
    kombi[10] += list(komb(word, kbdss, "_"))
    kombi[11] = list(komb(word, years))
    kombi[11] += list(komb(word, years, "_"))
    kombi[12] = [""]
    kombi[13] = [""]
    kombi[14] = [""]
    kombi[15] = [""]
    kombi[16] = [""]
    kombi[21] = [""]
    if profile["randnum"]:
        kombi[12] = list(concats(word, numfrom, numto))
        kombi[13] = list(concats(kombinaa, numfrom, numto))
        kombi[14] = list(concats(kombinaac, numfrom, numto))
        kombi[15] = list(concats(kombinaaw, numfrom, numto))
        kombi[16] = list(concats(kombinaak, numfrom, numto))
        kombi[21] = list(concats(reverse, numfrom, numto))
    kombi[17] = list(komb(reverse, years))
    kombi[17] += list(komb(reverse, years, "_"))
    kombi[18] = list(komb(rev_w, wbdss))
    kombi[18] += list(komb(rev_w, wbdss, "_"))
    kombi[19] = list(komb(rev_k, kbdss))
    kombi[19] += list(komb(rev_k, kbdss, "_"))
    kombi[20] = list(komb(rev_n, bdss))
    kombi[20] += list(komb(rev_n, bdss, "_"))
    komb001 = [""]
    komb002 = [""]
    komb003 = [""]
    komb004 = [""]
    komb005 = [""]
    komb006 = [""]
    if len(profile["spechars"]) > 0:
        komb001 = list(komb(kombinaa, profile["spechars"]))
        komb002 = list(komb(kombinaac, profile["spechars"]))
        komb003 = list(komb(kombinaaw, profile["spechars"]))
        komb004 = list(komb(kombinaak, profile["spechars"]))
        komb005 = list(komb(word, profile["spechars"]))
        komb006 = list(komb(reverse, profile["spechars"]))

    terminal("i", "Sorting list and removing duplicates...", newline=False)

    komb_unique = {}
    for i in range(1, 22):
        komb_unique[i] = list(dict.fromkeys(kombi[i]).keys())

    komb_unique01 = list(dict.fromkeys(kombinaa).keys())
    komb_unique02 = list(dict.fromkeys(kombinaac).keys())
    komb_unique03 = list(dict.fromkeys(kombinaaw).keys())
    komb_unique04 = list(dict.fromkeys(kombinaak).keys())
    komb_unique05 = list(dict.fromkeys(word).keys())
    komb_unique07 = list(dict.fromkeys(komb001).keys())
    komb_unique08 = list(dict.fromkeys(komb002).keys())
    komb_unique09 = list(dict.fromkeys(komb003).keys())
    komb_unique010 = list(dict.fromkeys(komb004).keys())
    komb_unique011 = list(dict.fromkeys(komb005).keys())
    komb_unique012 = list(dict.fromkeys(komb006).keys())

    uniqlist = (
        bdss
        + wbdss
        + kbdss
        + reverse
        + komb_unique01
        + komb_unique02
        + komb_unique03
        + komb_unique04
        + komb_unique05
    )

    for i in range(1, 21):
        uniqlist += komb_unique[i]

    uniqlist += (
        komb_unique07
        + komb_unique08
        + komb_unique09
        + komb_unique010
        + komb_unique011
        + komb_unique012
    )
    unique_list = list(dict.fromkeys(uniqlist).keys())
    unique_leet = []
    if profile["leetmode"]:
        for x in unique_list:
            for letter, leetletter in {"a": "4", "i": "1", "e": "3", "t": "7", "o": "0", "s": "5", "g": "9", "z": "2"}.items():
                x = x.replace(letter, leetletter)
            unique_leet.append(x)

    unique_list_finished = [
        x
        for x in unique_list + unique_leet
        if len(x) < 12 and len(x) > 5
    ]

    print_to_file(f"output/password_generator/{profile['name']}.txt", unique_list_finished)