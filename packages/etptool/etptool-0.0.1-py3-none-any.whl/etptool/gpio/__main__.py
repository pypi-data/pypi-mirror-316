"""GPIO commands

Author  : Jabez Winston <jabezwinston@gmail.com>
License : MIT
Date    : 18 December 2024

"""

import sys
import etplib

etp: etplib.ETP

def info(args):
    print(f"{etp.gpio.get_info()}")

def init(args):
    for arg in args:
        pin, mode = arg.split(":")
        etp.gpio.init({pin: {"mode": mode}})

def write(args):
    for arg in args:
        pin, state = arg.split(":")
        # Convert state to boolean
        state = state.lower()
        if state == "high" or state == "1" or state == "on" or state == "true":
            state = 1
        elif state == "low" or state == "0" or state == "off" or state == "false":
            state = 0

        etp.gpio.init({pin: {"mode": "output"}})
        etp.gpio.write({pin: state})

def read(args):
    if args[0] == "--monitor":
        etp.gpio.init({pin: {"mode": "input"} for pin in args[1:]})
        while True:
            try:
                states = etp.gpio.read(args[1:])
                sys.stdout.write(str(states) + "\r")
                sys.stdout.flush()
            except KeyboardInterrupt:
                sys.stdout.write("\n")
                break
    else:
        print(etp.gpio.read(args))

def main():
    global etp
    if len(sys.argv) > 2 and sys.argv[1] == "gpio":
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