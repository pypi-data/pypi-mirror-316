"""
Copyright (C) 2024, Jabez Winston C

Embedded Tester Protocol Tool

Author  : Jabez Winston C <jabezwinston@gmail.com>
License : MIT
Date    : 20-Sep-2024

"""

from .version import VERSION

import os
import platform
import sys
import runpy
import configparser
import argparse

import etplib

etp = None

def etp_run_subcmd(module):
    global etp
    runpy.run_module(f"etptool.{module}", run_name="__main__", alter_sys=True, init_globals={"etp": etp})

def create_config_file_if_needed():
    config = configparser.ConfigParser()
    CFG_PATH = os.path.join(os.path.dirname(__file__), 'etptool.cfg')
    if not os.path.exists(CFG_PATH):
        config.add_section('transport')
        config['transport'] = {
            'type': 'serial',
            'baudrate': '115200'
        }

        if platform.system() == 'Windows':
            config['transport']['port'] = 'COM3'
        elif platform.system() == 'Linux':
            config['transport']['port'] = '/dev/ttyACM0'
        elif platform.system() == 'Darwin':
            config['transport']['port'] = '/dev/tty.usbserial-0001'

        with open(CFG_PATH, 'w') as configfile:
            config.write(configfile)

def main():
    global etp

    create_config_file_if_needed()
    config = configparser.ConfigParser()
    CFG_PATH = os.path.join(os.path.dirname(__file__), 'etptool.cfg')
    config.read(CFG_PATH)
    transport = config['transport']['type']

    if transport == 'serial':
        etp = etplib.ETP(transport=config['transport']['type'], port=config['transport']['port'], baudrate=int(config['transport']['baudrate']))
    elif transport == 'tcp':
        etp = etplib.ETP(transport=config['transport']['type'], ip=config['transport']['ip'], port=int(config['transport']['port']))

    etp.open()
    etp.reset()
    # Check argv[1] for sub-module
    if len(sys.argv) > 1:
        module = sys.argv[1]
        etp_run_subcmd(module)
    else:
        print(f"Embedded Tester Protocol Tool - etptool v{VERSION}")
        print("Specify any of the below sub-commands:")
        sub_cmds = []
        # List all sub-modules (folders)
        for module in os.listdir(os.path.join(os.path.dirname(__file__))):
            if os.path.isdir(os.path.join(os.path.dirname(__file__), module)) and module[0] != '_':
                sub_cmds.append(module)

        sub_cmds.sort()
        for module in sub_cmds:
            print(f"  {module}")
        
    etp.close()

if __name__ == "__main__":
    main()
