"""PWM commands

Author  : Jabez Winston <jabezwinston@gmail.com>
License : MIT
Date    : 18 December 2024
"""

import sys
import etplib

etp: etplib.ETP

def info(args):
    print(f"{etp.pwm.get_info()}")

def init(args):
    for arg in args:
        pin, enable = arg.split(":")
        enable = enable.lower()
        if enable == "1" or enable == "true" or enable == "on" or enable == "en":
            enable = True
        else:
            enable = False
        etp.pwm.init({pin: enable})

def ctrl(args):
    for arg in args:
        pin, duty_cycle = arg.split(":")
        etp.pwm.init({pin: True})        # TODO : To be removed
        etp.pwm.ctrl(pin, duty_cycle)

def main():
    global etp
    if len(sys.argv) > 2 and sys.argv[1] == "pwm":
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