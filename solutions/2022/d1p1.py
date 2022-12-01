"""
Part 1

Last edited: 2022-12-01
"""
import time
import sys
import fileinput as fi

def run(data, io_time):
    t_start = time.perf_counter_ns()
    elfs = [0]
    for line in data:
        if line == '':
            elfs.append(0)
            continue
        elfs[-1] += int(line.rstrip())
    answer = max(elfs)
    t_stop = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_stop-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = list(line.rstrip() for line in fi.input())
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)

