"""
02-12-2021
Part 2

Authors: Wilhelm Ågren <wagren@kth.se>
Last edited: 02-12-2021
"""
import time
import sys
import fileinput as fi

def run(data, io_time):
    t_start = time.perf_counter_ns()
    mapping = dict(aim=0, y=0, x=0)
    for line in data:
        direction, amount = line.split(' ')
        if direction == 'forward':
            mapping['y'] += mapping['aim']*int(amount)
            mapping['x'] += int(amount)
        elif direction == 'up':
            mapping['aim'] -= int(amount)
        elif direction == 'down':
            mapping['aim'] += int(amount)
    answer = mapping['y']*mapping['x']
    t_stop = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_stop-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = list(line.rstrip() for line in fi.input())
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)

