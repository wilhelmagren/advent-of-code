"""Template for the adventofcode package pipeline.
Replace answer=None with your solution.
"""
import time
import sys
import fileinput as fi

from collections import defaultdict


def pythagorean(y, ey, x, ex):
    return (y-ey)**2 + (x-ex)**2


class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.f = 0
        self.g = 0
        self.h = 0

    def __eq__(self, other):
        return self.position == other.position


def bounds(arg, HEIGHT, WIDTH):
    y,x = arg
    return (0<=y) and (y<HEIGHT) and (0<=x) and (x<WIDTH)


def astar(graph, start, end):
    HEIGHT = len(graph)
    WIDTH = len(graph[0])
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    openlist = []
    closedlist = []
    openlist.append(start_node)

    while openlist:
        curr = openlist[0]
        curr_idx = 0
    
        # Get the node in open set that has shortest theoretical path to end
        for idx, node in enumerate(openlist):
            if node.f < curr.f:
                curr = node
                curr_idx = idx
    
        # Mark the current node with shortest distance as explored, move to closed
        openlist.pop(curr_idx)
        closedlist.append(curr)

        if curr == end_node:
            path = []
            while curr:
                path.append(curr.position)
                curr = curr.parent
            return path[::-1]
        
        # Generate children
        children = []

        adjacents = [(-1,0), (0,-1), (0,1), (1,0)]                
        for adj in adjacents:
            npos = (curr.position[0]+adj[0], curr.position[1]+adj[1])

            if not bounds(npos, HEIGHT, WIDTH):
                continue

            children.append(Node(curr, npos))
        
        for child in children:
            for closed in closedlist:
                if closed == child:
                    continue

            # Calculate heuristical distances
            child.g = curr.g + 1
            """
            child.h = pythagorean(child.position[0], end_node.position[0], child.position[1],
                    end_node.position[1])
            """
            child.h = int(graph[child.position[0]][child.position[1]])
            print(child.h)
            child.f = child.g + child.h

            for opened in openlist:
                if child == opened and child.g > opened.g:
                    continue

            openlist.append(child)




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
                    if new_w < old_w:
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
    data = list(line.rstrip() for line in fi.input())
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)

