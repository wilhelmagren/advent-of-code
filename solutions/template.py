"""
"""
import time
import sys
from aoc import data_generator, write_times

def run(data):
    pass
  
if __name__ == '__main__':
    datafile = sys.argv[1]
    t_io_start = time.perf_counter_ns()
    data = list(data_generator(datafile))
    t_io_end = time.perf_counter_ns()
    t_start = time.perf_counter_ns()
    answer = run(data)
    t_end = time.perf_counter_ns()
    io_time = (t_io_end-t_io_start)/1000000
    solve_time = (t_end-t_start)/1000000
    print(f'answer: {answer}')
    print(f'io time: {(t_io_end-t_io_start)/1000000} ms')
    print(f'solve time: {(t_end-t_start)/1000000} ms')
    print(f'total time: {io_time + solve_time} ms')
    write_times(io_time, solve_time)

