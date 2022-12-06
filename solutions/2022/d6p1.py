"""
Part 1.

Last edited: 2022-12-05
"""
import time
import sys
import fileinput as fi
from collections import defaultdict

def run(data, io_time):
    t_start = time.perf_counter_ns()
    row = data[0]
    cope = 4
    for char in range(4, len(row)):
        chars = row[char-4:char]
        if len(set(chars)) == 4:
            cope = char
            break
    answer = cope
    t_stop = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_stop-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = list(line.rstrip() for line in fi.input())
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)
