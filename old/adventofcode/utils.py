"""Global utility functions as part of the adventofcode package.
Contains four classes for: default values, valid files, printing, & colours.

Public functions in this file:
    $ query_user(str, str, str)     =>  bool
    $ get_ydp(PosixPath)            =>  tuple
    $ validate_arg(Namespace)       =>  dict

Private utility functions:
    $ _valid(str, list)             =>  bool


Authors: Wilhelm Ågren <wagren@kth.se>
Last edited: 07-12-2021
"""

import sys
import os
import datetime

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

def get_ydp(solutionpath):
    string = solutionpath.parts[-1]
    year = solutionpath.parts[-2]
    string = string.split('.')
    part = string[0][-1]
    day = ''.join(string[0].split('p')[0][1:])
    return year, day, part

def validate_args(args):
    arg_dict = vars(args)
    for key, val in arg_dict.items():
        if not _valid(key, val):
            raise ValueError(
                    f'{key=} argument is not valid, {val=}')
    return arg_dict

def _valid(key, vals):
    if key in ('verbose', 'setup', 'run'):
        return True
    mapping = dict(years=defaults.YEARS, days=defaults.DAYS, parts=defaults.PARTS)
    requirements = [
            all(map(lambda x: x in mapping[key], vals)),
            len(vals) <= len(mapping[key]),
            all(map(lambda x: type(x) is str, vals))
            ]
    return all(requirements)


