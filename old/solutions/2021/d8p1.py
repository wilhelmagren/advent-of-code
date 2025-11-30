"""
08-12-2021
Part 1

Author: Wilhelm Ågren <wagren@kth.se>
Last edited: 08-12-2021
"""
import time
import sys
import fileinput as fi

def run(data, io_time):
    t_start = time.perf_counter_ns()
    sumofnums = 0
    for line in data:
        line = line.split(' ')
        for string in line[11:]:
            lent = len(string)
            if lent == 2 or lent == 4 or lent == 3 or lent == 7:
                sumofnums += 1
    answer = int(sumofnums)
    t_stop = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_stop-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data  = list(line.rstrip() for line in fi.input())
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)

