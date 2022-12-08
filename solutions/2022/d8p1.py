"""
Part 1

Last edited: 2022-12-08
"""
import time
import sys
import fileinput as fi
import numpy as np
from collections import defaultdict

def run(data, io_time):
    t_start = time.perf_counter_ns()
    data = np.array([[int(c) for c in row] for row in data])

    HEIGHT = data.shape[0]
    WIDTH = data.shape[1]

    mask = np.full(data.shape, False)
    left = defaultdict(list)
    right = defaultdict(list)
    up = defaultdict(list)
    down = defaultdict(list)

    for y in range(HEIGHT):
        left[y].append(data[y, 0])
        right[y].append(data[y, WIDTH - 1])
        mask[y, 0] = True
        mask[y, WIDTH - 1] = True
        for x in range(WIDTH):
            l_curr = data[y, x]
            r_curr = data[y, WIDTH - 1 - x]
            if left[y][-1] < l_curr:
                left[y].append(l_curr)
                mask[y, x] = True
            if right[y][-1] < r_curr:
                right[y].append(r_curr)
                mask[y, WIDTH - 1 - x] = True

    for x in range(WIDTH):
        up[x].append(data[HEIGHT - 1, x])
        down[x].append(data[0, x])
        mask[HEIGHT - 1, x] = True
        mask[0, x] = True
        for y in range(HEIGHT):
            u_curr = data[HEIGHT - 1 - y, x]
            d_curr = data[y, x]
            if up[x][-1] < u_curr:
                up[x].append(u_curr)
                mask[HEIGHT - 1 - y, x] = True
            if down[x][-1] < d_curr:
                down[x].append(d_curr)
                mask[y, x] = True

    answer = mask.sum()
    
    t_stop = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_stop-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = list(line.rstrip() for line in fi.input())
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)

