"""
"""

import sys
import os
import datetime
import six.moves

from io import StringIO


class colours:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    END = '\033[0m'
    BOLD = '\033[1m'

class defaults:
    DAYS = list(str(day) for day in range(1, 26))
    YEARS = list(str(year) for year in range(2015, datetime.date.today().year + 1))
    PARTS = list(str(part) for part in range(1, 3))

class validfiles:
    DATA = list(f'd{day}.in' for day in defaults.DAYS)
    SOLUTION = list(f'd{day}p{part}.py' for day in defaults.DAYS for part in defaults.PARTS)

def VPRINT(msg):
    sys.stdout.write(f'{colours.BOLD}{colours.GREEN}[*]{colours.END}  {msg}\n')

def WPRINT(msg):
    sys.stdout.write(f'{colours.BOLD}{colours.YELLOW}[!]{colours.END}  {msg}\n')

def EPRINT(msg):
    sys.stderr.write(f'{colours.BOLD}{colours.RED}[X]{colours.END}  {msg}\n')

class printer:
    ERROR = EPRINT
    WORKING = VPRINT
    WARNING = WPRINT

def query_user(true, false, msg):
    response = input(f'{colours.BOLD}{colours.GREEN}[*]{colours.END}  {msg}')
    return response == true

