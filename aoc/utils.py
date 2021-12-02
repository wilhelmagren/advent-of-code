import os
import sys

from .solutions import Solutions

DEFAULTS = dict(y=range(2018, 2022),
                d=range(1, 26),
                p=range(1, 3),
                precision='ms')

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

def format_datafile(problem):
    splitted = problem.split('d')
    day, part = splitted[1].split('p')
    year = splitted[0][1:]
    return f'data/{year}/d{day}p{part}.dat'

def check_problems(problems):
    return list(problem for problem in problems if exists(problem))

def get_datafiles(problems):
    return list(format_datafile(problem) for problem in problems)

def generator(fname, mode='r'):
    with open(fname, mode) as f:
        for line in f.readlines():
            yield line.rstrip()

