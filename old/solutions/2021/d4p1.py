"""
04-12-2021
Part 1

Authors: Wilhelm Ågren <wagren@kth.se>
Last edited: 04-12-2021
"""
import time
import sys
import fileinput as fi


def _create_bingo(data):
    boards = list()
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
    for yidx, row in enumerate(board):
        if all(list(',True' in item for item in row)):
            return True
    for xidx in range(len(board[0])):
        column = list()
        for yidx in range(len(board)):
            column.append(board[yidx][xidx])
        if all(list(',True' in item for item in column)):
            return True
    return False

def _sumofnums(board):
    sumofnums = 0
    for yidx, row in enumerate(board):
        for xidx, item in enumerate(row):
            if ',True' not in item:
                val = int(item.split(',')[0])
                sumofnums += val
    return sumofnums

def run(data, io_time):
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
                sumofnums = _sumofnums(board)
                answer = int(number) * sumofnums
                foundbingo = True
    t_stop = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_stop-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = list(line.rstrip() for line in fi.input())
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)

