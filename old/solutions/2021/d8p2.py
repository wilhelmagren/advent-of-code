"""
08-12-2021
Part 2

Author: Wilhelm Ågren <wagren@kth.se>
Last edited: 08-12-2021
"""
import time
import sys
import fileinput as fi
from itertools import permutations

def run(data, io_time):
    t_start = time.perf_counter_ns()
    numbers=list()
    for idx, line in enumerate(data):
        line = line.split(' ')
        mapping = dict()
        stack = list()
        for string in line[:10]:
            stack.append(string)
        stack.sort(key=len)
        kukone = [[0,1],[1,0]]
        fouriter = [[1,3], [3,1]]
        eightiter = [[4,6], [6,4]]
        breaker = False
        breakerb = False
        for hora in kukone:
            if breakerb:
                break
            for xdfour in fouriter:
                if breaker:
                    break
                for xdeight in eightiter:
                    for idx, string in enumerate(stack):
                        if idx == 0:
                            xd1, xd2 = hora
                            mapping[2] = string[xd1]
                            mapping[5] = string[xd2]
                        if idx == 1:
                            mapping[0] = string.replace(mapping[2],'').replace(mapping[5],'')
                        if idx == 2:
                            for kuk, s in zip(xdfour, string.replace(mapping[2],'').replace(mapping[5],'')):
                                mapping[kuk] = s
                        if idx == 9:
                            for kuk, s in zip(xdeight, string.replace(mapping[2],'').replace(mapping[5],'').replace(mapping[1],'').replace(mapping[3],'').replace(mapping[0],'')):
                                mapping[kuk] = s
                    number = ''
                    zero = mapping[0]+mapping[1]+mapping[2]+mapping[4]+mapping[5]+mapping[6]
                    one = mapping[2]+mapping[5]
                    two = mapping[0]+mapping[2]+mapping[3]+mapping[4]+mapping[6]
                    three = mapping[0]+mapping[2]+mapping[3]+mapping[5]+mapping[6]
                    four = mapping[1]+mapping[2]+mapping[3]+mapping[5]
                    five = mapping[0]+mapping[1]+mapping[3]+mapping[5]+mapping[6]
                    six = mapping[0]+mapping[1]+mapping[3]+mapping[4]+mapping[5]+mapping[6]
                    seven = mapping[0]+mapping[2]+mapping[5]
                    eight = ''.join(mapping.values())
                    nine = ''.join(mapping.values()).replace(mapping[4],'')
                    numbermap = {zero:'0',one:'1', two:'2', three:'3', four:'4', five:'5', six:'6',seven:'7',eight:'8',nine:'9'}
                    num = ''
                    for string in line[11:]:
                        for perm in [''.join(p) for p in permutations(string)]:
                            val = numbermap.get(perm, None)
                            if val:
                                num += val
                                break
                    if len(num) == 4:
                        breaker = True
                        breakerb = True
                        numbers.append(num)
                        break

    answer = int(sum(map(lambda x: int(x), numbers)))
    t_stop = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_stop-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = list(line.rstrip() for line in fi.input())
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)

