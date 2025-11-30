"""
05-12-2021
Part 1

Authors: Wilhelm Ågren <wagren@kth.se>
Last edited: 05-12-2021
"""
import time
import sys
import fileinput as fi

from collections import defaultdict

def run(data, io_time):
    t_start = time.perf_counter_ns()
    mapping = defaultdict(int)
    for line in data:
        split = line.split(' ')
        x1,y1 = list(map(lambda x: int(x), split[0].split(',')))
        x2,y2 = list(map(lambda x: int(x), split[2].split(',')))
        if x1 == x2:
            for y in range(min(y1,y2), max(y1,y2)+1):
                mapping[(x1,y)] += 1
        elif y1 == y2:
            for x in range(min(x1,x2), max(x1,x2)+1):
                mapping[(x,y1)] += 1
    answer = sum(map(lambda x: 1 if x >= 2 else 0, mapping.values()))
    t_stop = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_stop-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = list(line.rstrip() for line in fi.input())
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)

