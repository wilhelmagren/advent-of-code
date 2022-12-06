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

    rows = defaultdict(list)

    rows[1].extend(list(reversed(['N', 'W', 'B'])))
    rows[2].extend(list(reversed(['B', 'M', 'D', 'T', 'P', 'S', 'Z', 'L'])))
    rows[3].extend(list(reversed(['R', 'W', 'Z', 'H', 'Q'])))
    rows[4].extend(list(reversed(['R', 'Z', 'J', 'V', 'D', 'W'])))
    rows[5].extend(list(reversed(['B', 'M', 'H', 'S'])))
    rows[6].extend(list(reversed(['B', 'P', 'V', 'H', 'J', 'N', 'G', 'L'])))
    rows[7].extend(list(reversed(['S', 'L', 'D', 'H', 'F', 'Z', 'Q', 'J'])))
    rows[8].extend(list(reversed(['B', 'Q', 'G', 'J', 'F', 'S', 'W'])))
    rows[9].extend(list(reversed(['J', 'D', 'C', 'S', 'M', 'W', 'Z'])))

    for i in range(10, len(data)):
        nummove = int(data[i].split(' ')[1])
        frommove = int(data[i].split(' ')[3])
        tomove = int(data[i].split(' ')[5])
        popped = [rows[frommove].pop() for _ in range(nummove)]
        rows[tomove].extend(popped)

    answer = ''.join([rows[i].pop() for i in range(1, 10)])
    t_stop = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_stop-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = list(line.rstrip() for line in fi.input())
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)
