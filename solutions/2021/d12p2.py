"""Template for the adventofcode package pipeline.
Replace answer=None with your solution.
"""
import time
import sys
import fileinput as fi
import copy

from collections import defaultdict, Counter

class Graph:
    def __init__(self, data):
        self.create_graph(data)

    def create_graph(self, data):
        dic = defaultdict(list)
        for line in data:
            u, v = line.split('-')
            if u == 'start':
                dic[u].append(v)
            elif v == 'start':
                dic[v].append(u)
            else:
                if u == 'end':
                    dic[v].append(u)
                else:
                    dic[u].append(v)
                    dic[v].append(u)

        self.g = dic
        self.numpaths = 0
        self.paths = []
        self.found = False
   
    def rec(self, u, visited, path):
        if u == 'end':
            self.numpaths += 1
            self.paths.append(path)
            return
        counter = Counter(visited)
        something_2times = True if any([val >= 2 for _, val in counter.items()]) else False
        for v in self.g[u]:
            pcop = copy.deepcopy(path)
            vcop = copy.deepcopy(visited)
            if something_2times:
                if v in vcop:
                    continue
            if v.islower() and v != 'start' and v != 'end':
                vcop.append(v)
            pcop.append(v) 
            self.rec(v, vcop, pcop)

    def x(self):
        u = 'start'
        self.rec(u, [], [])

def run(data, io_time):
    t_start = time.perf_counter_ns()
    G = Graph(data)
    G.x()
    answer = G.numpaths
    t_end = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_end-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = list(line.rstrip() for line in fi.input())
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)

