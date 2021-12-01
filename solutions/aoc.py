import os
import sys
import numpy as np

MAX_DAYS = 25
MAX_PARTS = 2
DEFAULT_DAYS = range(1, MAX_DAYS + 1)
DEFAULT_PARTS = range(1, MAX_PARTS + 1)
precision_map = {
        'second': ' s',
        'milli': 'ms',
        'micro': '\u03BCs',
        'nano': 'ns'}

precision_scale = {
        'second': 1000000000,
        'milli': 1000000,
        'micro': 1000,
        'nano': 1}


class Statistics:
    def __init__(self, parts, precision, *args, **kwargs):
        self.n_parts = len(parts)
        self.precision = precision
        self.data = list()

    def __str__(self):
        return ''
    
    def _scale(self, data):
        return data / precision_scale[self.precision]

    def update(self, d):
        d = self._scale(d)
        self.data.append(d)
        print(f'approximate time: {d}{precision_map[self.precision]}')

    def calculate(self):
        argmax = np.argmax(self.data) 
        argmin = np.argmin(self.data)
        variance = np.var(self.data)
        mean = np.mean(self.data)
        
        max_day = argmax // self.n_parts
        min_day = argmin // self.n_parts
        max_part = argmax % self.n_parts
        min_part = argmin % self.n_parts

        print(f'\ncalculating sufficient statistics based on solved problems')
        print(f'----------------------------------------------------------')
        print(f'slowest: day {max_day+1} part {max_part+1}')
        print(f'fastest: day {min_day+1} part {min_part+1}')
        print(f'variance: {np.round(variance, 4)}')
        print(f'mean: {np.round(mean, 4)}')


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

def valid_stats(stats):
    return stats in ['second', 'milli', 'micro', 'nano']

def data_generator(fname):
    with open(fname, 'r') as f:
        for line in f.readlines():
            yield int(line.rstrip())

