"""Template for the adventofcode package pipeline.
Replace answer=None with your solution.
"""
import time
import sys
import fileinput as fi

def run(data, io_time):
    t_start = time.perf_counter_ns()
    def _solve(l):
        for id1, d1 in enumerate(l):
            for id2, d2 in enumerate(l[id1:]):
                for id3, d3 in enumerate(l[id2:]):
                    if int(d1)+int(d2)+int(d3)==2020:
                        return int(d1)*int(d2)*int(d3)
    answer = _solve(data)
    t_end = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_end-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = list(line.rstrip() for line in fi.input())
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)

