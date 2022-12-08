"""
Part 2

Last edited: 2022-12-08
"""
import time
import sys
import fileinput as fi
import numpy as np
from collections import defaultdict

def _num_until_larger(arr):
    hook = arr[0]
    for i in range(1, len(arr)):
        if arr[i] >= hook: return i
    return len(arr) - 1

def _num_until_larger_inv(arr):
    hook = arr[-1]
    for i in reversed(range(0, len(arr) - 1)):
        if arr[i] >= hook: return len(arr) - 1 - i
    return len(arr) - 1

def run(data, io_time):
    t_start = time.perf_counter_ns()
    # data = "30373\n25512\n65332\n33549\n35390".split('\n')
    data = np.array([[int(c) for c in row] for row in data])

    HEIGHT = data.shape[0]
    WIDTH = data.shape[1]

    scores = defaultdict(str)
    for y in range(1, HEIGHT - 1):
        for x in range(1, WIDTH - 1):
            _str = str(y) + str(x)
            a = _num_until_larger(data[y, x:WIDTH])
            b = _num_until_larger_inv(data[y, 0:x+1])
            c = _num_until_larger(data[y:HEIGHT, x])
            d = _num_until_larger_inv(data[0:y+1, x])
            # print(a, b, c, d)
            scores[_str] = a * b * c * d
    
    answer = max(scores.values())

    t_stop = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_stop-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = list(line.rstrip() for line in fi.input())
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)

