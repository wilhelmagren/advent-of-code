"""

As the submarine drops below the surface of the ocean, it automatically performs a sonar sweep of the nearby sea floor. On a small screen, the sonar sweep report (your puzzle input) appears: each line is a measurement of the sea floor depth as the sweep looks further and further away from the submarine.

For example, suppose you had the following report:

199
200
208
210
200
207
240
269
260
263

This report indicates that, scanning outward from the submarine, the sonar sweep found depths of 199, 200, 208, 210, and so on.

The first order of business is to figure out how quickly the depth increases, just so you know what you're dealing with - you never know if the keys will get carried into deeper water by an ocean current or a fish or something.

To do this, count the number of times a depth measurement increases from the previous measurement. (There is no measurement before the first measurement.) In the example above, the changes are as follows:

199 (N/A - no previous measurement)
200 (increased)
208 (increased)
210 (increased)
200 (decreased)
207 (increased)
240 (increased)
269 (increased)
260 (decreased)
263 (increased)

In this example, there are 7 measurements that are larger than the previous measurement.

How many measurements are larger than the previous measurement?
"""
import time
import sys
from aoc import data_generator, write_times

def run(data):
    return sum(list(map(lambda x: 1 if int(data[x]) > int(data[x-1]) else 0, range(1, len(data)))))

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

