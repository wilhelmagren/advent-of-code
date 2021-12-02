import argparse

from aoc.solutions import Solutions
from aoc.utils import generator, intify, validate, check_problems, format_problems, get_datafiles, DEFAULTS

def parse_args():
    parser = argparse.ArgumentParser(prog='AoC pipeline', usage='%(prog)s year(s) day(s) part(s) [options]')
    parser.add_argument('-y', '--years', nargs='*', dest='years',
            default=DEFAULTS['y'], help='set what AoC years to solve problems from')
    parser.add_argument('-d', '--days', nargs='*', dest='days',
            default=DEFAULTS['d'], help='set what days to solve')
    parser.add_argument('-p', '--parts', nargs='*', dest='parts',
            default=DEFAULTS['p'], help='set what parts of a day to solve')
    args = parser.parse_args()
    return args

def validate_args(args):
    years = intify(args.years)
    days = intify(args.days)
    parts = intify(args.parts)

    if not validate(years, 'y'):
        raise ValueError

    if not validate(days, 'd'):
        raise ValueError

    if not validate(parts, 'p'):
        raise ValueError

    problems = check_problems(format_problems(years, days, parts))
    datafiles = get_datafiles(problems)
    return (problems, datafiles)

if __name__ == '__main__':
    args = parse_args()
    problems, datafiles = validate_args(args)
    solutions = Solutions()
    for problem, datafile in zip(problems, datafiles):
        data = list(generator(datafile, mode='r'))
        print(getattr(solutions, problem)(data))

