import argparse
import warnings
import time
import os
import sys
import subprocess

from solutions.aoc import intify, stringify, valid_days, valid_parts, valid_stats, DEFAULT_DAYS, DEFAULT_PARTS, VPRINT
from solutions.aoc import Statistics
warnings.filterwarnings('ignore', category=UserWarning)

def parse_args():
    parser = argparse.ArgumentParser(prog='AoC2021 pipieline', usage='%(prog)s [days] [parts] [options]')
    parser.add_argument('-d', '--days', nargs='*', dest='days',
            default=DEFAULT_DAYS, help='set what days to solve', required=True)
    parser.add_argument('-s', '--stats', dest='stats', nargs=1,
            help='set precision for benchmarking stats')
    parser.add_argument('-p', '--parts', nargs='*', dest='parts',
            default=DEFAULT_PARTS, help='set which parts of a day to solve', required=True)
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
            help='set logging in verbose mode')
    args = parser.parse_args()
    return validate_args(args)

def validate_args(args):
    days = intify(args.days)
    parts = intify(args.parts)
    verbose = args.verbose
    stats = args.stats

    if not valid_days(days):
        raise ValueError(f'invalid formatting on what days to solve! days={days}')

    if not valid_parts(parts):
        raise ValueError(f'invalid formatting on what parts to solve! parts={parts}')
    
    if stats:
        stats = stats[0]
        if not valid_stats(stats):
            raise ValueError(f'invalid formatting for statistics precision! stats={stats}')

    return dict(verbose=verbose, days=days, parts=parts, stats=stats)
    
def _solve(day, part, verbose, statistics):
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
    approximate_execution_time = t_end - t_start
    statistics.update(approximate_execution_time)
    return approximate_execution_time

def solve(args):
    days = args['days']
    parts = args['parts']
    verbose = args['verbose']
    statistics = Statistics(parts, args['stats'])

    list(_solve(day, part, verbose, statistics) for day in days for part in parts)
    return statistics

if __name__ == '__main__':
    args = parse_args()
    statistics = solve(args)
    if args['stats']:
        statistics.calculate()

