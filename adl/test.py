#!/usr/bin/env python3

import sys
import os
import time
from subprocess import call

# Initializes the command line parser
try:
    from argparse import ArgumentParser, RawDescriptionHelpFormatter
except ImportError:
    print("[Error] Library argparse missing")
    sys.exit(-1)

from adl import ADL

# Checks the input file
def check_input(filename):
    if not os.path.exists(filename):
        print(str(filename) + " does not exist")
        sys.exit(-1)
    if not os.path.isfile(filename):
        print(str(filename) + " is a directory")
        sys.exit(-1)


# Parses the command line arguments and options
def options():
    epilog = "All arguments and options are mandatory"
    # The RawDescriptionHelpFormatter is required to show the epilog
    parser = ArgumentParser(epilog=epilog, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("input", metavar="\"INPUT\"", default="", help="source file")
    args = parser.parse_args()
    # Converts the list of options to a dictionary
    opts = args.__dict__
    if opts['input'] is "":
        parser.error("Input file is missing.")
    return opts


if __name__ == '__main__':
    
    # Gets the start time
    start_time = time.time()
    # Prints a message
    print("Running ...")
    # Retrieves the command line arguments and options
    opts = options()
    check_input(opts["input"])
    # Retrieves the content of the source file
    src_file = open(opts["input"], "r")
    file_content = src_file.read()
    src_file.close()
    
    # Parses the source file
    scenario = ADL.parse(file_content)
    
    # Cleans bytecode
    call('find . -name "*.pyc" -exec rm -rf {} \;', shell=True)
    call('find . -name "parsetab.py" -exec rm -rf {} \;', shell=True)
    
    # Prints a message
    print("Done")
    # Logs the execution time
