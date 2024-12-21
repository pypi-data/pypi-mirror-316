"""Firwmare commands

Author  : Jabez Winston <jabezwinston@gmail.com>
License : MIT
Date    : 20 December 2024
"""
import sys
import etplib

etp: etplib.ETP

def info(args):
    print(etp.get_fw_info()) 

def main():
    global etp
    if len(sys.argv) > 2 and sys.argv[1] == "fw":
        func = getattr(sys.modules[__name__], sys.argv[2])
        if len(sys.argv) > 3:
            func(sys.argv[3:])
        else:
            func([])
    elif len(sys.argv) == 2:
        print("No command specified")
    else:
        print("Invalid command")

if __name__ == "__main__":
    main()
