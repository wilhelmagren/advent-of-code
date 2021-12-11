"""Template for the adventofcode package pipeline.
Replace answer=None with your solution.
"""
import time
import sys
import fileinput as fi


class Board:
    def __init__(self, data):
        self.data = data
        self.HEIGHT = len(data)
        self.WIDTH = len(data[0])
        self.flashes = 0
        self.allflashed = False

    def _quake(self, y, x, hasflashed):
        neighbours = [(y-1,x-1),(y-1,x),(y-1,x+1),(y,x-1),(y,x+1),(y+1,x-1),(y+1,x),(y+1,x+1)] 
        for y,x in neighbours:
            if self.bounds(y,x):
                self.data[y][x] += 1

        for y, x in neighbours:
            if self.bounds(y,x):
                flashed = hasflashed.get((y,x), None)
                if not flashed:
                    if self.data[y][x] > 9:
                        hasflashed[(y,x)] = True
                        self.flashes += 1
                        self._quake(y,x, hasflashed)
    
    def step(self):
        hasflashed = {}
        for yidx in range(self.HEIGHT):
            for xidx in range(self.WIDTH):
                self.data[yidx][xidx] += 1

        for yidx in range(self.HEIGHT):
            for xidx in range(self.WIDTH):
                flashed = hasflashed.get((yidx,xidx), None)
                if not flashed:
                    if self.data[yidx][xidx] > 9:
                        hasflashed[(yidx,xidx)] = True
                        self.flashes += 1
                        self._quake(yidx, xidx, hasflashed)

        for y, x in hasflashed:
            self.data[y][x] = 0

        if len(hasflashed) == self.HEIGHT*self.WIDTH:
            self.allflashed = True


    def bounds(self, yidx, xidx):
        return (0 <= yidx) and (yidx < self.HEIGHT) and (0 <= xidx) and (xidx < self.WIDTH)



def run(data, io_time):
    t_start = time.perf_counter_ns()
    board = Board(data)
    steps = 0
    while True:
        if board.allflashed:
            break
        steps += 1
        board.step()
    answer = steps
    t_end = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_end-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = list(line.rstrip() for line in fi.input())
    #data = "5483143223\n2745854711\n5264556173\n6141336146\n6357385478\n4167524645\n2176841721\n6882881134\n4846848554\n5283751526".split('\n')
    xd = []
    for line in data:
        xd.append([])
        for c in line:
            xd[-1].append(int(c))
    data = xd
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)

