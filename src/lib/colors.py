# Color terminal
r = "\033[31m"
g = "\033[32m"
y = "\033[33m"
b = "\033[34m"
p = "\033[35m"
d = "\033[2;37m"
w = "\033[0m"

W = f"{w}\033[1;47m"
R = f"{w}\033[1;41m"
G = f"{w}\033[1;42m"
Y = f"{w}\033[1;43m"
B = f"{w}\033[1;44m"
space = "    "
des_space = "⁣  ⁣⁣  ⁣⁣ "
lines = space + "—"*85

OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
BOLD = '\033[1m'
ENDC = '\033[0m'

class Terminal:
    ...