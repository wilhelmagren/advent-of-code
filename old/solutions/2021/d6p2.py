"""
06-12-2021
Part 2

Authors: Wilhelm Ågren <wagren@kth.se>
Last edited: 06-12-2021
"""
import time
import sys
import fileinput as fi

from collections import defaultdict


def run(data, io_time):
    t_start = time.perf_counter_ns()
    timers = defaultdict(int)
    for val in data[0].split(','):
        timers[int(val)] += 1
    for day in range(256):
        updated_timers = defaultdict(int)
        for timer, number in timers.items():
            if timer > 0:
                updated_timers[timer-1] = number
        updated_timers[6] += timers[0]
        updated_timers[8] += timers[0]
        timers = updated_timers
    answer = sum(timers.values())
    t_stop = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_stop-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = list(line.rstrip() for line in fi.input())
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)

