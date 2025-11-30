import argparse
import os
import sys

from adventofcode.solver import Solver
from adventofcode.utils import defaults, printer, validate_args
from adventofcode.setup import setup_dirs, find_sessiontoken
from adventofcode.datautil import request


def argparser(*args, **kwargs):
    parser = argparse.ArgumentParser(prog='python aoc.py',
                        description='Streamlined Advent of Code pipeline so that you can help save christmas as easily as possible!',
                        epilog='We have to save christmas!',
                        argument_default=None)
    parser.add_argument('-v', '--verbose', action='store_true',
                        dest='verbose', help='print time-stats for your solutions')
    parser.add_argument('-s', '--setup', action='store_true',
                        dest='setup', help='setup the required directory structures')
    parser.add_argument('-r', '--run', action='store_true',
                        dest='run', help='run the solver on your solutions')
    parser.add_argument('-y', '--years', nargs='*', dest='years',
                        default=defaults.YEARS, help='set what years to solve problems from')
    parser.add_argument('-d', '--days', nargs='*', dest='days',
                        default=defaults.DAYS, help='set what days to solve')
    parser.add_argument('-p', '--parts', nargs='*', dest='parts',
                        default=defaults.PARTS, help='set what parts of a day to solve')
    return parser.parse_args()

if __name__ == '__main__':
    args = argparser()
    args = validate_args(args)
    solver = Solver(args)
    sessiontoken = find_sessiontoken()
    if not sessiontoken:
        printer.ERROR(f'could not find a `session.token` file in the root directory of this file.\n     Any http GET requests for input data from https://adventofcode.com/ will be unsuccessful ...')
    else:
        printer.WORKING(f'using `{sessiontoken.parts[-1]}` as cookie for http GET request if data file is missing.')
    if args['setup']:
        setup_dirs()
    if args['run']:
        solver.run(log_success=True)
        if args['verbose']:
            solver.stats()
        else:
            solver.answers()

