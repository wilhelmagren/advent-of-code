"""Template for the adventofcode package pipeline.
Replace answer=None with your solution.
"""
import time
import sys
import fileinput as fi

def run(data, io_time):
    t_start = time.perf_counter_ns()
    lowpoints = list()
    HEIGHT = len(data) 
    WIDTH = len(data[0])
    data = ''.join([s for s in data])
    for idx, char in enumerate(data):
        if idx == 0:
            if int(char) < int(data[idx+1]) and int(char) < int(data[idx+WIDTH]):
                lowpoints.append(int(char)+1)
        elif idx == WIDTH-1:
            if int(char) < int(data[idx-1]) and int(char) < int(data[idx+WIDTH]):
                lowpoints.append(int(char)+1)
        elif idx == HEIGHT*WIDTH-WIDTH:
            if int(char) < int(data[idx-WIDTH]) and int(char) < int(data[idx+1]):
                lowpoints.append(int(char)+1)
        elif idx == HEIGHT*WIDTH-1:
            if int(char) < int(data[idx-WIDTH]) and int(char) < int(data[idx-1]):
                lowpoints.append(int(char)+1)
        else:
            if idx % WIDTH == 0:
                if int(char) < int(data[idx+1]) and int(char) < int(data[idx-WIDTH]) and int(char) < int(data[idx+WIDTH]):
                    lowpoints.append(int(char)+1)
            elif idx // HEIGHT == 0:
                if int(char) < int(data[idx-1]) and int(char) < int(data[idx+1]) and int(char) < int(data[idx+WIDTH]):
                    lowpoints.append(int(char)+1)
            elif idx % WIDTH == WIDTH-1:
                if int(char) < int(data[idx-1]) and int(char) < int(data[idx-WIDTH]) and int(char) < int(data[idx+WIDTH]):
                    lowpoints.append(int(char)+1)
            elif idx // WIDTH == HEIGHT-1:
                if int(char) < int(data[idx-1]) and int(char) < int(data[idx+1]) and int(char) < int(data[idx-WIDTH]):
                    lowpoints.append(int(char)+1)
            else:
                if int(char) < int(data[idx+1]) and int(char) < int(data[idx-1]) and int(char) < int(data[idx+WIDTH]) and int(char) < int(data[idx-WIDTH]):
                    lowpoints.append(int(char)+1)

    answer = sum(lowpoints)
    t_end = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_end-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = list(line.rstrip() for line in fi.input())
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)

