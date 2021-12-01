import argparse
import warnings
import time
import os
import sys
import subprocess

from aocio import intify, stringify, valid_days, valid_parts, DEFAULT_DAYS, DEFAULT_PARTS, VPRINT
warnings.filterwarnings('ignore', category=UserWarning)

def parse_args():
    parser = argparse.ArgumentParser(prog='AoC2021 pipieline', usage='%(prog)s [days] [parts] [options]')
    parser.add_argument('-d', '--days', nargs='*', dest='days',
        default=DEFAULT_DAYS, help='set what days to solve')
    parser.add_argument('-p', '--parts', nargs='*', dest='parts',
        default=DEFAULT_PARTS, help='set which parts of a day to solve')
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
        help='set logging in verbose mode')
    args = parser.parse_args()
    return validate_args(args)

def validate_args(args):
    days = intify(args.days)
    parts = intify(args.parts)
    verbose = args.verbose

    if not valid_days(days):
        raise ValueError(f'invalid formatting on what days to solve! days={days}')

    if not valid_parts(parts):
        raise ValueError(f'invalid formatting on what parts to solve! parts={parts}')

    return dict(verbose=verbose, days=days, parts=parts)
    
def _solve(day, part, verbose):
    VPRINT(f'\nSolving day={day:02d} part={part}', verbose)
    VPRINT(f'---------------------', verbose)
    solver_file = stringify(day, part)
    data_file = stringify(day)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    solver_file = os.path.join(dir_path, f'solutions/{solver_file}')
    data_file = os.path.join(dir_path, f'solutions/{data_file}')
    t_start = time.perf_counter_ns()
    os.system(f'python3 {solver_file} {data_file}')
    t_end = time.perf_counter_ns()
    return t_end - t_start


def solve(args):
    days = args['days']
    parts = args['parts']
    verbose = args['verbose']

    return list(_solve(day, part, verbose) for part in parts for day in days)

if __name__ == '__main__':
    args = parse_args()
    times = solve(args)
    print(times)
