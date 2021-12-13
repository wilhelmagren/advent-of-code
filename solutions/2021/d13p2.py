"""Template for the adventofcode package pipeline.
Replace answer=None with your solution.
"""
import time
import sys
import fileinput as fi

from collections import defaultdict

def write_letters(mapping):
    x_coords = [x for x,_ in mapping]
    y_coords = [y for _,y in mapping]
    x_coords.sort()
    y_coords.sort()
    WIDTH = x_coords[-1] + 1
    HEIGHT = y_coords[-1] + 1
    s = ''
    with open('output.txt', 'w') as f:
        for y in range(HEIGHT):
            s += '\n'
            for x in range(WIDTH):
                gotted = mapping.get((x,y), False)
                if gotted:
                    s += '#'
                else:
                    s += '.'
        f.write(s)


def fold_y(mapping, pos):
    keys = list(k for k in mapping.keys())
    for x,y in keys:
        if y > pos:
            newpos = y-pos
            mapping[(x,pos-newpos)] = True
            mapping = dict(mapping)
            del mapping[(x,y)]
    return mapping

def fold_x(mapping, pos):
    keys = [k for k in mapping.keys()]
    for x,y in keys:
        if x > pos:
            newpos = x-pos
            mapping[(pos-newpos,y)] = True
            mapping = dict(mapping)
            del mapping[(x,y)]
    return mapping

def run(data, io_time):
    t_start = time.perf_counter_ns()
    mapping = defaultdict(bool)
    splits = []
    for line in data:
        linelen = len(line)
        if linelen == 0:
            continue
        if linelen < 11:
            x,y = line.split(',')
            mapping[(int(x),int(y))] = True
        elif linelen >= 11:
            where = line.split(' ')[2]
            pos, amnt = where.split('=')
            splits.append((pos, int(amnt)))

    for pos, amnt in splits:
        if pos == 'y':
            mapping = fold_y(mapping, amnt)
        if pos == 'x':
            mapping = fold_x(mapping, amnt)

    """
    for (x,y), val in mapping.items():
        if val:
            print(x,y)
    """
    marked = sum(map(lambda x: int(x), mapping.values()))
    answer = marked
    write_letters(mapping)
    t_end = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_end-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = list(line.rstrip() for line in fi.input())
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)

