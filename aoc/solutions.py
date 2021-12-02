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

from collections import defaultdict


class Solutions(object):
    def __init__(self, *args, **kwargs):
        pass

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

