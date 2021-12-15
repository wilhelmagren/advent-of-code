"""Template for the adventofcode package pipeline.
Replace answer=None with your solution.
"""
import time
import sys
import fileinput as fi

from collections import defaultdict


class Graph:
    def __init__(self, data):
        self._setup(data)

    def _setup(self, data):
        # The argument of a defaultdict will be called when you try to access a key that 
        # doesn't exist. If you try to access edges[key_not_exist] you will get a 
        # defaultdict(list), and if you try to access even deeper, i.e. 
        # edges[key_not_exist][key_not_exist] you will get 0, default int value.
        edges = defaultdict(lambda: defaultdict(int))
        adjacents = defaultdict(list)
        self.WIDTH = len(data[0])
        self.HEIGHT = len(data)
        self.NUM_VERTICES = self.WIDTH*self.HEIGHT
        edges = [[] for _ in range(self.NUM_VERTICES)]
        for y, line in enumerate(data):
            for x, num in enumerate(line):
                adj = [(y-1,x),(y,x-1),(y,x+1),(y+1,x)]
                for ey, ex in adj:
                    if self._bounds(ey,ex):
                        weight = float(int(data[ey][ex]) + int(num)) / 2
                        edges[x + y*self.WIDTH].append((ex + ey*self.WIDTH, weight))
        
        # Clean away all weights which are None
        edges = [[(idx, w) for (idx, w) in edges[idx] if w] for idx in range(self.NUM_VERTICES)]
        self.edges = edges
        self.visited = []

    def _bounds(self, *args):
        y,x = args
        return (0<=y) and (y<self.HEIGHT) and (0<=x) and (x<self.WIDTH)
    
    def astar(self, source=None, target=None):
        pass
    
    def dijkstra(self, source=None, target=None):
        from queue import PriorityQueue
        if not source:
            source = 0
        if not target:
            target = self.HEIGHT*self.WIDTH -1

        # Keep the shortest distance from source to all other vertices here
        D = {k: float('inf') for k in range(self.NUM_VERTICES)}
        D[0] = 0

        pq = PriorityQueue()
        pq.put((0, source))

        while not pq.empty():
            (w, curr) = pq.get()

            if curr == target:
                return w

            self.visited.append(curr)
            for adj, dist in self.edges[curr]:
                if adj not in self.visited:
                    old_w = D[adj]
                    new_w = D[curr] + dist
                    if new_w <= old_w:
                        pq.put((new_w, adj))
                        D[adj] = new_w

        return D[target]
        


def run(data, io_time):
    t_start = time.perf_counter_ns()
    G = Graph(data)
    answer = int(G.dijkstra())
    t_end = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_end-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = [line.rstrip() for line in fi.input()]
    """
    data = "1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581".split('\n')
    """
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)

