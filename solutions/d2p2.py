"""
--- Part Two ---

Based on your calculations, the planned course doesn't seem to make any sense. You find the submarine manual and discover that the process is actually slightly more complicated.

In addition to horizontal position and depth, you'll also need to track a third value, aim, which also starts at 0. The commands also mean something entirely different than you first thought:

    down X increases your aim by X units.
    up X decreases your aim by X units.
    forward X does two things:
        It increases your horizontal position by X units.
        It increases your depth by your aim multiplied by X.

Again note that since you're on a submarine, down and up do the opposite of what you might expect: "down" means aiming in the positive direction.

Now, the above example does something different:

    forward 5 adds 5 to your horizontal position, a total of 5. Because your aim is 0, your depth does not change.
    down 5 adds 5 to your aim, resulting in a value of 5.
    forward 8 adds 8 to your horizontal position, a total of 13. Because your aim is 5, your depth increases by 8*5=40.
    up 3 decreases your aim by 3, resulting in a value of 2.
    down 8 adds 8 to your aim, resulting in a value of 10.
    forward 2 adds 2 to your horizontal position, a total of 15. Because your aim is 10, your depth increases by 2*10=20 to a total of 60.

After following these new instructions, you would have a horizontal position of 15 and a depth of 60. (Multiplying these produces 900.)

Using this new interpretation of the commands, calculate the horizontal position and depth you would have after following the planned course. What do you get if you multiply your final horizontal position by your final depth?
"""
import time
import sys
from aoc import data_generator, write_times

def run(data):
    # y, x, aim
    pos = [0, 0, 0]
    dirmap = {'down': (0, 1),
                'up': (0, -1),
                'forward': (1, 1)}
    for line in data:
        direction, amnt = line.split(' ')
        amnt = int(amnt)
        if direction == 'forward':
            pos[1] += amnt
            pos[0] += pos[2] * amnt
        elif direction == 'up':
            pos[2] -= amnt
        elif direction == 'down':
            pos[2] += amnt
    return pos[0]*pos[1]
 
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

