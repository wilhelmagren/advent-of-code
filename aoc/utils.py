"""utility function implementations for the AdventofCode (AoC) pipeline.
wow! take a look at that sexy banner, dont you want one as well?...
 - (https://patorjk.com/software/taag/#p=display&f=Slant&t=Advent%20of%20Code)

this file is a hot pile of garbage right now, but the functions gets the job done.
TODO: clean up some deprecated functions and look at adding some more times
        stats for each problem solution. make the code good...

Authors: Wilhelm Ågren <wagren@kth.se>
Last edited: 02-12-2021
"""
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

BANNER = f"""
{colors.BOLD}{colors.RED}
==========================================================================={colors.GREEN}
---------------------------------------------------------------------------{colors.END}
    ___       __                 __           ____   ______          __   
   /   | ____/ /   _____  ____  / /_   ____  / __/  / ____/___  ____/ /__ 
  / /| |/ __  / | / / _ \/ __ \/ __/  / __ \/ /_   / /   / __ \/ __  / _ \\
 / ___ / /_/ /| |/ /  __/ / / / /_   / /_/ / __/  / /___/ /_/ / /_/ /  __/
/_/  |_\__,_/ |___/\___/_/ /_/\__/   \____/_/     \____/\____/\__,_/\___/ 
{colors.GREEN}
---------------------------------------------------------------------------{colors.RED}
===========================================================================
{colors.END}
"""


def APRINT(s_t, d_t, decimals=3):
    s_t_ms = np.round(s_t / 1000_000, decimals)
    d_t_ms = np.round(d_t / 1000_000, decimals)
    t_t_ms = np.round(s_t_ms + d_t_ms, decimals)
    s_color = colors.GREEN
    d_color = colors.GREEN
    t_color = colors.GREEN
    # solution
    if 1. < s_t_ms < 10.:
        s_color = colors.YELLOW
    elif 10. <= s_t_ms:
        s_color = colors.RED
    # data reading io
    if .5 <= d_t_ms < 1.:
        d_color = colors.YELLOW
    elif 1. <= d_t_ms:
        d_color = colors.RED
    # total
    if 1. <= t_t_ms < 2.:
        t_color = colors.YELLOW
    elif 2. <= t_t_ms:
        t_color = colors.RED
    print(f'    {t_color}{t_t_ms:.3f} ms{colors.END}         {d_color}{d_t_ms:.3f} ms{colors.END}           {s_color}{s_t_ms:.3f} ms{colors.END}\n')

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

