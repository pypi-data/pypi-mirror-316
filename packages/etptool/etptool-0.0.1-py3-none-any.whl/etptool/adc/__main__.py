"""ADC commands

Author  : Jabez Winston <jabezwinston@gmail.com>
License : MIT
Date    : 18 December 2024
"""

import sys
import etplib

etp: etplib.ETP

def info(args):
    print(etp.adc.get_info())

def init(args):
    for arg in args:
        pin, mode = arg.split(":")
        if mode == "en" or mode == "true":
            etp.adc.init({pin: True})
        elif mode == "dis" or mode == "false":
            etp.adc.init({pin: False})

def read(args):
    if args[0] == "--monitor":
        etp.adc.init({pin: True for pin in args[1:]})
        while True:
            try:
                for pin in args[1:]:
                    sys.stdout.write(f"  {pin}: {etp.adc.read(pin)} \t")
                sys.stdout.write("\r")
            except KeyboardInterrupt:
                sys.stdout.write("\n")
                break
    else:
        for pin in args:
            print(f"{pin}: {etp.adc.read(pin)}")

def main():
    global etp
    if len(sys.argv) > 2 and sys.argv[1] == "adc":
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