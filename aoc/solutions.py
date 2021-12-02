""" implementation of AoC solutions, all functions called from main file
which invokes the attribute of the class relating to the respective function.
all functions implementing a solution to an AoC problem should have the format

    `fYEARdDAYpPART` 

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

class Solutions(object):
    def __init__(self, *args, **kwargs):
        pass

    def f2020d1p1(self, data):
        data = _intify(data)
        for id1, d1 in enumerate(data):
            for id2, d2 in enumerate(data[id1:]):
                if d1+d2==2020:
                    return d1*d2

    def f2020d1p2(self, data):
        data = _intify(data)
        for id1, d1 in enumerate(data):
            for id2, d2 in enumerate(data[id1:]):
                for id3, d3 in enumerate(data[id2:]):
                    if d1+d2+d3==2020:
                        return d1*d2*d3

    def f2020d2p1(self, data):
        def _valid(num, char, pwd):
            count = Counter(pwd)
            if num[0] <= count.get(char, 0) <= num[1]:
                return 1
            return 0
        return sum(list(_valid(nums, char, pwd) for nums, char, pwd in _format(data)))
    
    def f2020d2p2(self, data):
        def _valid(nums, char, pwd):
            num1, num2 = nums
            if pwd[num1-1] is char and pwd[num2-1] is char:
                return 0
            elif pwd[num1-1] is char:
                return 1
            elif pwd[num2-1] is char:
                return 1
            return 0
        return sum(list(_valid(nums, char, pwd) for nums, char, pwd in _format(data)))

    def f2020d3p1(self, data):
        return _traverse((data, 1, 3))

    def f2020d3p2(self, data):
        setups = [(data, 1, 1), (data, 1, 3), (data, 1, 5), (data, 1, 7), (data, 2, 1)]
        def _mul(iterable):
            prod = 1
            for i in iterable:
                prod *= i
            return prod
        return _mul(list(map(_traverse, setups)))

    def f2021d1p1(self, data):
        return sum(list(map(lambda x: 1 if int(data[x]) > int(data[x-1]) else 0, range(1, len(data)))))

    def f2021d1p2(self, data):
        return sum(list(map(lambda x: 1 if int(data[x]) + int(data[x-1]) + int(data[x-2]) > int(data[x-1]) + int(data[x-2]) + int(data[x-3]) else 0, range(3, len(data)))))

    def f2021d2p1(self, data):
        mappings = {'forward': 0, 'down': 0, 'up': 0}
        for line in data:
            direction, amount = line.split(' ')
            mappings[direction] += int(amount)
        return (mappings['down']-mappings['up'])*mappings['forward']

    def f2021d2p2(self, data):
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
        return (mappings['y'] * mappings['x'])

    def f2021d3p1(self, data):
        raise NotImplementedError

    def f2021d3p2(self, data):
        raise NotImplementedError

