"""SPI commands

Author  : Jabez Winston <jabezwinston@gmail.com>
License : MIT
Date    : 18 December 2024
"""

import sys
import etplib
import etptool._helper.cli as cli

etp: etplib.ETP


def info(args):
    print(f"{etp.spi.get_info()}")

def init(args):
    # bus, speed, mode
    result = cli.parse_args({"bus": int, "speed": int, "mode": int}, args)
    etp.spi.init(result["bus"], result["speed"], result["mode"])

def transfer(args):
    # bus, data
    result = cli.parse_args({"bus": int, "data": list[int]}, args)
    etp.spi.init(0, 0, 1000)  # TODO: To be removed
    rx_data = etp.spi.transfer(result["bus"], result["data"])
    print(rx_data)

def main():
    global etp
    if len(sys.argv) > 2 and sys.argv[1] == "spi":
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