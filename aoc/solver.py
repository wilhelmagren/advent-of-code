""" implementation of AoC solutions, all functions called from main file
which invokes the attribute of the class relating to the respective function.
all functions implementing a solution to an AoC problem should have the format

    `f<YEAR>d<DAY>p<PART>` 

and expect one argument, the data which as been read from the corresponding 
problem datafile. the input data is a list of strings, one string for each
line of the datafile. parsing and casting to necessary datatype has to be 
done in respective function.


Authors: Wilhelm Ågren <wagren@kth.se>
Last edited: 02-12-2021
"""
import time
import os
import sys
import math
import random
import numpy as np

from collections import defaultdict, Counter


def _intify(iterable):
    return list(int(item) for item in iterable)

def _format(iterable):
        formatted = list(((int(row.split(' ')[0].split('-')[0]), int(row.split(' ')[0].split('-')[1])), row.split(' ')[1][0], row.split(' ')[2]) for row in iterable)
        return formatted

def _traverse(tple):
    iterable, ystride, xstride = tple
    trees, xpos, ypos = 0, 0, 0
    WIDTH = len(iterable[0])
    DEPTH = len(iterable)
    while ypos + ystride <= DEPTH -1:
        xpos += xstride
        ypos += ystride
        if xpos >= WIDTH:
            xpos -= WIDTH
        if iterable[ypos][xpos] == '#':
            trees +=1
    return trees

def _create_bingo(data):
    boards = list()
    count = 0
    for idx, line in enumerate(data):
        line = line.split()
        if not line:
            boards.append(list())
            continue
        boards[-1].append(line)
    return boards

def _mark(num, board):
    for yidx, row in enumerate(board):
        for xidx, val in enumerate(row):
            if num == val:
                board[yidx][xidx] += ',True'
def _hasbingo(board):
    for xidx, row in enumerate(board):
        if all(list(',True' in item for item in row)):
            return True
    for xidx in range(len(board[0])):
        column = list()
        for yidx in range(len(board)):
            column.append(board[yidx][xidx])
        if all(list(',True' in item for item in column)):
            return True
    return False

def _sumofnumbers(board):
    summer = 0
    for yidx, row in enumerate(board):
        for xidx, item in enumerate(row):
            if ',True' not in item:
                val = int(item.split(',')[0])
                summer += val
    return summer
            
class Solutions:

    def f2020d1p1(self, data):
        t_start = time.perf_counter_ns()
        data = _intify(data)
        for id1, d1 in enumerate(data):
            for id2, d2 in enumerate(data[id1:]):
                if d1+d2==2020:
                    t_stop = time.perf_counter_ns()
                    return (d1*d2, t_stop-t_start)

    def f2020d1p2(self, data):
        t_start = time.perf_counter_ns()
        data = _intify(data)
        for id1, d1 in enumerate(data):
            for id2, d2 in enumerate(data[id1:]):
                for id3, d3 in enumerate(data[id2:]):
                    if d1+d2+d3==2020:
                        t_stop = time.perf_counter_ns()
                        return (d1*d2*d3, t_stop-t_start)

    def f2020d2p1(self, data):
        t_start = time.perf_counter_ns()
        def _valid(num, char, pwd):
            count = Counter(pwd)
            if num[0] <= count.get(char, 0) <= num[1]:
                return 1
            return 0
        answer = sum(list(_valid(nums, char, pwd) for nums, char, pwd in _format(data)))
        t_stop = time.perf_counter_ns()
        return (answer, t_stop-t_start)
    
    def f2020d2p2(self, data):
        t_start = time.perf_counter_ns()
        def _valid(nums, char, pwd):
            num1, num2 = nums
            if pwd[num1-1] is char and pwd[num2-1] is char:
                return 0
            elif pwd[num1-1] is char:
                return 1
            elif pwd[num2-1] is char:
                return 1
            return 0
        answer = sum(list(_valid(nums, char, pwd) for nums, char, pwd in _format(data)))
        t_stop = time.perf_counter_ns()
        return (answer, t_stop-t_start)

    def f2020d3p1(self, data):
        t_start = time.perf_counter_ns()
        answer = _traverse((data, 1, 3))
        t_stop = time.perf_counter_ns()
        return (answer, t_stop-t_start)

    def f2020d3p2(self, data):
        t_start = time.perf_counter_ns()
        setups = [(data, 1, 1), (data, 1, 3), (data, 1, 5), (data, 1, 7), (data, 2, 1)]
        def _mul(iterable):
            prod = 1
            for i in iterable:
                prod *= i
            return prod
        answer = _mul(list(map(_traverse, setups)))
        t_stop = time.perf_counter_ns()
        return (answer, t_stop-t_start)

    def f2021d1p1(self, data):
        t_start = time.perf_counter_ns()
        answer = sum(list(map(lambda x: 1 if int(data[x]) > int(data[x-1]) else 0, range(1, len(data)))))
        t_stop = time.perf_counter_ns()
        return (answer, t_stop-t_start)

    def f2021d1p2(self, data):
        t_start = time.perf_counter_ns()
        answer = sum(list(map(lambda x: 1 if int(data[x]) + int(data[x-1]) + int(data[x-2]) > int(data[x-1]) + int(data[x-2]) + int(data[x-3]) else 0, range(3, len(data)))))
        t_stop = time.perf_counter_ns()
        return (answer, t_stop-t_start)

    def f2021d2p1(self, data):
        t_start = time.perf_counter_ns()
        mappings = {'forward': 0, 'down': 0, 'up': 0}
        for line in data:
            direction, amount = line.split(' ')
            mappings[direction] += int(amount)
        answer = (mappings['down']-mappings['up'])*mappings['forward']
        t_stop = time.perf_counter_ns()
        return (answer, t_stop-t_start)

    def f2021d2p2(self, data):
        t_start = time.perf_counter_ns()
        mappings = {'aim': 0, 'y': 0, 'x': 0}
        for line in data:
            direction, amount = line.split(' ')
            if direction == 'forward':
                mappings['y'] += mappings['aim'] * int(amount)
                mappings['x'] += int(amount)
            elif direction == 'up':
                mappings['aim'] -= int(amount)
            elif direction == 'down':
                mappings['aim'] += int(amount)
        answer = mappings['y'] * mappings['x']
        t_stop = time.perf_counter_ns()
        return (answer, t_stop-t_start)

    def f2021d3p1(self, data):
        t_start = time.perf_counter_ns()
        bitlen = len(data[0])
        amounts = defaultdict(list)
        for line in data:
            for idx, char in enumerate(line):
                amounts[idx].append(int(char))
        gamma = ''
        for key, vals in amounts.items():
            gamma += '1' if sum(vals) > int(len(vals)/2) else '0'

        epsilon = int(gamma,2)^int(''+'1'*bitlen,2)
        answer = int(gamma,2)*epsilon
        t_stop = time.perf_counter_ns()
        return (answer, t_stop-t_start)

    def f2021d3p2(self, data):
        t_start = time.perf_counter_ns()
        def _rec(iterable, bitidx, oxygen):
            if len(iterable) == 1:
                return iterable[0]
            more_ones = 0
            for item in iterable:
                if item[bitidx] == '1':
                    more_ones += 1
            char = None
            if oxygen:
                more_ones = more_ones >= (len(iterable) - more_ones)
                char = '1' if more_ones else '0'
            else:
                more_ones = more_ones < (len(iterable) - more_ones)
                char = '1' if more_ones else '0'
            return _rec(list(item for item in iterable if item[bitidx] == char), bitidx+1, oxygen)

        outputs = list(int(_rec(data, 0, bol), 2) for bol in [True, False])
        answer = outputs[0]*outputs[1]
        t_stop = time.perf_counter_ns()
        return (answer, t_stop-t_start)

    def f2021d4p1(self, data):
        t_start = time.perf_counter_ns()
        numbers = data[0].split(',')
        boards = _create_bingo(data[1:])
        foundbingo = False
        answer = None
        for number in numbers:
            if foundbingo:
                break
            for board in boards:
                _mark(number, board)
                if _hasbingo(board):
                    sumonum = _sumofnumbers(board)
                    answer = int(number) * sumonum
                    foundbingo = True
        t_stop = time.perf_counter_ns()
        return (answer, t_stop-t_start)
    
    def f2021d4p2(self, data):
        t_start = time.perf_counter_ns()
        numbers = data[0].split(',')
        boards = _create_bingo(data[1:])
        foundbingo = False
        answer = None
        winboards = list()
        for number in numbers:
            for board in boards:
                if _hasbingo(board):
                    continue
                _mark(number, board)
                if _hasbingo(board):
                    sumonum = _sumofnumbers(board)
                    answer = int(number) * sumonum
                    winboards.append(answer)
        winboards = list(item for item in winboards if item != 0)
        answer = winboards[-1]
        t_stop = time.perf_counter_ns()
        return (answer, t_stop-t_start)

    def f2021d5p1(self, data):
        t_start = time.perf_counter_ns()
        mapping = defaultdict(int)
        for line in data:
            split = line.split(' ')
            x1,y1 = list(map(lambda x: int(x), split[0].split(',')))
            x2,y2 = list(map(lambda x: int(x), split[2].split(',')))
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    mapping[(x1, y)] += 1
            elif y1 == y2:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    mapping[(x, y1)] += 1

        answer = sum(list(map(lambda x: 1 if x >= 2 else 0, mapping.values())))
        t_stop = time.perf_counter_ns()
        return (answer, t_stop-t_start)

    def f2021d5p2(self, data):
        t_start = time.perf_counter_ns()
        mapping = defaultdict(int)
        for line in data:
            split = line.split(' ')
            x1,y1 = list(map(lambda x: int(x), split[0].split(',')))
            x2,y2 = list(map(lambda x: int(x), split[2].split(',')))
            if x1 == x2:
                # Vertical
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    mapping[(x1, y)] += 1
            
            elif y1 == y2:
                # Horizontal
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    mapping[(x, y1)] += 1
            elif np.abs(x1-x2) == np.abs(y1-y2):
                # Diagonal
                xarange = range(x1, x2 + 1 if x2 > x1 else x2 - 1, 1 if x2 > x1 else -1)
                yarange = range(y1, y2 + 1 if y2 > y1 else y2 - 1, 1 if y2 > y1 else -1)
                for x, y in zip(xarange, yarange):
                    mapping[(x,y)] += 1
        answer = sum(list(map(lambda x: 1 if x >= 2 else 0, mapping.values())))
        t_stop = time.perf_counter_ns()
        return (answer, t_stop-t_start)

