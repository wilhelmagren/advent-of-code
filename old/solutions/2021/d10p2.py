"""
10-12-2021
Part 2

Author: Wilhelm Ågren <wagren@kth.se>
Last edited: 10-12-2021
"""
import time
import sys
import fileinput as fi

def run(data, io_time):
    t_start = time.perf_counter_ns()
    scores = {')': 1, ']': 2, '}': 3, '>': 4}
    c2o = {')':'(', ']':'[','}':'{','>':'<'}
    o2c = {'(':')', '[':']','{':'}','<':'>'}
    corrections = []
    for line in data:
        openingstack = []
        breaker = False
        for char in line:
            if char not in o2c:
                if openingstack[-1] != c2o[char]:
                    breaker = True
                else:
                    openingstack.pop()
            else:
                openingstack.append(char)
        if breaker:
            continue
        sumofcompleted = 0
        openingstack.reverse()
        for opener in openingstack:
            sumofcompleted *= 5
            sumofcompleted += scores[o2c[opener]]
        corrections.append(sumofcompleted)
    corrections.sort()
    answer = corrections[int((len(corrections)-1)/2)]
    t_end = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_end-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = list(line.rstrip() for line in fi.input())
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)

