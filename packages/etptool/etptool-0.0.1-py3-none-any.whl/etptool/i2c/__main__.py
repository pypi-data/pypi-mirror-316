"""I2C commands

Author  : Jabez Winston <jabezwinston@gmail.com>
License : MIT
Date    : 18 December 2024
"""

import sys
import argparse
import etplib
import etptool._helper.cli as cli

etp: etplib.ETP

def info(args):
    print(f"{etp.i2c.get_info()}")

def init(args):
    # bus, speed
    result = cli.parse_args({"bus": int, "speed": int}, args)
    etp.i2c.init(result["bus"], result["speed"])

def scan(args):
    # bus
    result = cli.parse_args({"bus": int}, args)
    etp.i2c.init(result["bus"], 100)   # TODO: To be removed
    print(etp.i2c.scan(result["bus"]))

def read(args):
    # bus, addr, len
    result = cli.parse_args({"bus": int, "addr": int, "len": int}, args)
    etp.i2c.init(result["bus"], 100)   # TODO: To be removed
    print(etp.i2c.read(result["bus"], result["addr"], result["len"]))

def write(args):
    # bus, addr, data
    result = cli.parse_args({"bus": int, "addr": int, "data": list[int]}, args)
    etp.i2c.init(result["bus"], 100)   # TODO: To be removed
    etp.i2c.write(result["bus"], result["addr"], result["data"])


def read_reg(args):
    # bus, addr, reg, len
    result = cli.parse_args({"bus": int, "addr": int, "reg": int, "len": int}, args)
    etp.i2c.init(result["bus"], 100)   # TODO: To be removed
    print(etp.i2c.read_reg(result["bus"], result["addr"], result["reg"], result["len"]))

def write_reg(args):
    # bus, addr, reg, data
    result = cli.parse_args({"bus": int, "addr": int, "reg": int, "data": list[int]}, args)
    etp.i2c.init(result["bus"], 100)   # TODO: To be removed
    print(result)
    etp.i2c.write_reg(result["bus"], result["addr"], result["reg"], result["data"])

def main():
    global etp
    if len(sys.argv) > 2 and sys.argv[1] == "i2c":
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