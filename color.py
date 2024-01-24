#!python3
import sys

help_msg = (f"Usage: {sys.argv[0]} [-h|--help] [-g|--grey|--gray] [-c|--compact] [-d|--decimal]\n"
            "-h, --help\t\tShow this help.\n"
            "-g, --grey, --gray\tUse greyscale instead of RGB colour.\n"
            "-c, --compact\t\tInput RGB value as one compact value.\n"
            "-d, --decimal\t\tUse decimal instead of hex for input values.")


def get_input(str_hint):
    while True:
        print(str_hint, end="")
        x = input()
        if len(x) == 0:
            continue
        elif (x[0] == 'q') | (x[0] == 'Q'):
            exit(0)
        else:
            try:
                hex_x = int(x, int_format)
            except ValueError:
                continue
            return hex_x


print("==== Terminal Color Printer ====")
greyscale = False
compact = False
int_format = 16
for i in range(1, len(sys.argv)):
    if (sys.argv[i] == "-h") | (sys.argv[i] == "--help"):
        print(help_msg)
        exit(0)
    if (sys.argv[i] == "-g") | (sys.argv[i] == "--grey") | (sys.argv[i] == "--gray"):
        greyscale = True
    if (sys.argv[i] == "-c") | (sys.argv[i] == "--compact"):
        compact = True
    if (sys.argv[i] == "-d") | (sys.argv[i] == "--decimal"):
        int_format = 10


text = "▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇"
while True:
    if greyscale:
        grey = get_input("Greyscale: ")
        red = green = blue = grey
    elif compact:
        rgb = get_input("Red|Green|Blue: ")
        blue = rgb & 0xff
        rgb >>= 8
        green = rgb & 0xff
        rgb >>= 8
        red = rgb & 0xff
    else:
        red = get_input("Red: ")
        green = get_input("Green: ")
        blue = get_input("Blue: ")
    print(f'\033[38;2;{red};{green};{blue}m{text}\033[0m')
    print("--------------------------------")
