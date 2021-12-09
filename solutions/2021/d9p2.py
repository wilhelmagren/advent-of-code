"""Template for the adventofcode package pipeline.
Replace answer=None with your solution.
"""
import time
import sys
import fileinput as fi
import numpy as np

from collections import defaultdict
from collections.abc import Iterable

def flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, tuple):
            yield from flatten(el)
        else:
            yield el

class Board:
    def __init__(self, data, *args, **kwargs):
        self.data = np.array([[int(c) for c in line] for line in data]).astype(np.int8)
        self.basins = defaultdict(list)

    def basinsize(self, existing, yidx, xidx):
        iterator = [(yidx-1,xidx), (yidx,xidx-1), (yidx+1,xidx), (yidx,xidx+1)]
        basinlist = []
        for y, x in iterator:
            if self.inbounds(y, x):
                if self[y, x] != 9:
                    if existing.get((y,x)):
                        continue
                    existing[(y,x)] = True
                    basinlist.append((y,x))
        accum = [self.basinsize(existing, y,x) for y,x in basinlist]
        return basinlist + accum

    def solve(self):
        sizes = list()
        visited = {}
        for yidx in range(self.shape[0]):
            for xidx in range(self.shape[1]):
                if self[yidx, xidx] == 9:
                    continue
                lolxd = list(set(flatten(self.basinsize(visited, yidx, xidx) + [(yidx, xidx)])))
                #print('----------------------------')
                #print(f'{xidx=}, {yidx=}, {lolxd}')
                sizes.append(len(lolxd))
                #print(f'size={sizes[-1]}')
        sizes.sort(reverse=True)
        return sizes[0]*sizes[1]*sizes[2]

    def __getitem__(self, coordinate):
        yidx, xidx = coordinate
        if self.inbounds(yidx, xidx):
            return self.data[yidx, xidx]

    def inbounds(self, yidx, xidx):
        if 0 <= yidx < self.data.shape[0] and 0 <= xidx < self.data.shape[1]:
            return True
        return False

    @property
    def shape(self):
        return self.data.shape

def run(data, io_time):
    t_start = time.perf_counter_ns()
    b = Board(data)
    answer = b.solve()
    t_end = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_end-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = list(line.rstrip() for line in fi.input())
    #data = "2199943210\n3987894921\n9856789892\n8767896789\n9899965678".split('\n')
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)

