#!python3
import sys
import paramiko

help_msg = (f"Usage: {sys.argv[0]} [-h|--help] [-g|--grey|--gray] [-c|--compact] [-d|--decimal]\n"
            "-h, --help\t\tShow this help.\n"
            "")

print("==== SSH Tunnel Forward Tool ====")
for i in range(1, len(sys.argv)):
    if (sys.argv[i] == "-h") | (sys.argv[i] == "--help"):
        print(help_msg)
        exit(0)

