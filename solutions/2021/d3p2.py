"""
03-12-2021
Part 2

Authors: Wilhelm Ågren <wagren@kth.se>
Last edited: 03-12-2021
"""
import time
import sys
import fileinput as fi

def run(data, io_time):
    t_start = time.perf_counter_ns()
    def _rec(iterable, bitidx, oxygen):
        if len(iterable) == 1:
            return iterable[0]
        ones = 0
        for item in iterable:
            if item[bitidx] == '1':
                ones += 1
        char = None
        if oxygen:
            char = '1' if ones >= (len(iterable) - ones) else '0'
        else:
            char = '1' if ones < (len(iterable) - ones) else '0'
        return _rec(list(item for item in iterable if item[bitidx] == char), bitidx+1, oxygen)
    outputs = list(int(_rec(data, 0, bol), 2) for bol in [True, False])
    answer = outputs[0]*outputs[1]
    t_stop = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_stop-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = list(line.rstrip() for line in fi.input())
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)

