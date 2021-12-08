"""
02-12-2021
Part 1

Authors: Wilhelm Ågren <wagren@kth.se>
Last edited: 02-12-2021
"""
import time
import sys
import fileinput as fi

def run(data, io_time):
    t_start = time.perf_counter_ns()
    mapping = dict(forward=0, down=0, up=0)
    for line in data:
        direction, amount = line.split(' ')
        mapping[direction] += int(amount)
    answer = (mapping['down']-mapping['up'])*mapping['forward']
    t_stop = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_stop-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = list(line.rstrip() for line in fi.input())
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)

