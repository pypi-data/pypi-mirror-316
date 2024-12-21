"""SPI commands

Author  : Jabez Winston <jabezwinston@gmail.com>
License : MIT
Date    : 18 December 2024
"""

import sys
import etplib
import configparser

etp: etplib.ETP

def save(args):
    config = configparser.ConfigParser()
    # Arguments:
    # transport serial:COM4:115200
    # transport tcp:IP:port
    CFG_PATH = 'etptool/etptool.cfg'

    if args[0] == 'transport':
        config.add_section('transport')
        transport, port, baudrate = args[1].split(':')
        if transport == 'serial':
            config['transport'] = {
                'type': transport,
                'port': port,
                'baudrate': baudrate
            }
        elif transport == 'tcp':
            config['transport'] = {
                'type': transport,
                'ip': port,
                'port': baudrate
            }

    with open(CFG_PATH, 'w') as configfile:
        config.write(configfile)

def main():
    global etp
    if len(sys.argv) > 2 and sys.argv[1] == "cfg":
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