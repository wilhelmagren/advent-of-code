"""implementation of AoC pipeline, manually pick what years, days, and parts
you want to solve through the CLI or just run all possible by not specifying.
if there exists a solution implementation to a problem, the solver expects
there to be a corresponding data file in data/<YEAR>/ which it can read input
from. otherwise the pipeline will crash. yeah, though luck kiddo...

Authors: Wilhelm Ågren <wagren@kth.se>
Last edited: 02-12-2021
"""
import argparse

from aoc.solutions import Solutions
from aoc.utils import colors, generator, intify, validate, get_ydp, check_problems, format_problems, get_datafiles, DEFAULTS, APRINT


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
        year, day, part = get_ydp(problem)
        print(f'\n{colors.BOLD}Solving:  year={year}  day={int(day):02d}  part={part}')
        print(f'-----------------------------------{colors.END}')
        data = list(generator(datafile, mode='r'))
        (answer, t) = getattr(solutions, problem)(data)
        APRINT(answer, t)

