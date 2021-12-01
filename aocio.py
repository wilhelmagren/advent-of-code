import os
import sys

MAX_DAYS = 25
MAX_PARTS = 2
DEFAULT_DAYS = range(1, MAX_DAYS + 1)
DEFAULT_PARTS = range(1, MAX_PARTS + 1)

def VPRINT(msg, verbose):
    print(msg) if verbose else None

def stringify(day, part=None):
    if part is None:
        return f'd{day}data.txt'

    return f'd{day}p{part}.py'

def intify(l):
    return list(set(list(int(item) for item in l)))

def exists(part, tpe='d'):
    solutions = os.listdir('solutions/')
    for solution in solutions:
        if tpe+str(part) in solution:
            return True
    return False

def valid_days(days):
    requirements = [
            all(list(map(lambda x: x in DEFAULT_DAYS, days))),
            all(list(map(lambda x: type(x) is int, days))),
            len(days) <= MAX_DAYS,
            all(list(map(lambda x: exists(x, tpe='d'), days)))
            ]
    return all(requirements)

def valid_parts(parts):
    requirements = [
            all(list(map(lambda x: x in DEFAULT_PARTS, parts))),
            all(list(map(lambda x: type(x) is int, parts))),
            len(parts) <= MAX_PARTS,
            all(list(map(lambda x: exists(x, tpe='p'), parts)))
            ]
    return all(requirements)

"""
def data_generator(fname):
    with open(fname, 'r') as f:
        for line in f.readlines():
            yield int(line.rstrip())
"""

