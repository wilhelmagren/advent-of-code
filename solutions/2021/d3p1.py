"""
03-12-2021
Part 1

Authors: Wilhelm Ågren <wagren@kth.se>
Last edited: 03-12-2021
"""
import time
import sys
import fileinput as fi
from collections import defaultdict

def run(data, io_time):
    t_start = time.perf_counter_ns()
    bitlen = len(data[0])
    amounts = defaultdict(list)
    for line in data:
        for idx, char in enumerate(line):
            amounts[idx].append(int(char))
    gamma = ''
    for key, vals in amounts.items():
        gamma += '1' if sum(vals) > int(len(vals)/2) else '0'
    epsilon = int(gamma,2)^int(''+'1'*bitlen,2)
    answer = int(gamma,2)*epsilon
    t_stop = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_stop-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = list(line.rstrip() for line in fi.input())
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)

