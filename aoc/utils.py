import os
import sys
import numpy as np

from .solutions import Solutions

DEFAULTS = dict(y=range(2018, 2022),
                d=range(1, 26),
                p=range(1, 3),
                precision='ms')


class colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    END = '\033[0m'
    BOLD = '\033[1m'

def APRINT(answer, t, decimals=3):
    t_ms = np.round(t / 1000000, decimals)
    color = colors.GREEN

    print(f'[*] answer:\t{colors.BLUE}{answer}{colors.END}')
    if 10 <= t_ms < 250:
        color = colors.YELLOW
    elif 250 <= t_ms:
        color = colors.RED
    print(f'[*] time:\t{color}{t_ms} ms{colors.END}')

def validate(iterable, condition):
    requirements = [
        all(list(map(lambda x: x in DEFAULTS[condition], iterable))),
        len(iterable) <= len(DEFAULTS[condition])]
    return all(requirements)

def intify(iterable):
    return list(int(item) for item in iterable)

def exists(solution):
    return hasattr(Solutions, solution)

def format_problems(years, days, parts):
    return list(f'f{year}d{day}p{part}' for year in years for day in days for part in parts)

def get_ydp(problem):
    splitted = problem.split('d')
    day, part = splitted[1].split('p')
    year = splitted[0][1:]
    return (year, day, part)

def format_datafile(problem):
    year, day, part = get_ydp(problem)
    return f'data/{year}/d{day}p{part}.dat'

def check_problems(problems):
    return list(problem for problem in problems if exists(problem))

def get_datafiles(problems):
    return list(format_datafile(problem) for problem in problems)

def generator(fname, mode='r'):
    with open(fname, mode) as f:
        for line in f.readlines():
            yield line.rstrip()

