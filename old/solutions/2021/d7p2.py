"""
07-12-2021
Part 2

Authors: Wilhelm Ågren <wagren@kth.se>
Last edited: 07-12-2021
"""
import time
import sys
import fileinput as fi
import numpy as np



def run(data, io_time):
    t_start = time.perf_counter_ns()
    data = list(map(lambda x: int(x), data[0].split(',')))
    answer = min(list(sum(map(lambda x: int(np.abs(x-val)*(np.abs(x-val)+1)/2), data)) for val in data))
    t_stop = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_stop-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = list(line.rstrip() for line in fi.input())
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)

