"""implementation of AoC pipeline, manually pick what years, days, and parts
you want to solve through the CLI or just run all possible by not specifying.
if there exists a solution implementation to a problem, the solver expects
there to be a corresponding data file in data/<YEAR>/ which it can read input
from. otherwise the pipeline will crash. yeah, though luck kiddo...

Authors: Wilhelm Ågren <wagren@kth.se>
Last edited: 02-12-2021
"""
import argparse

from aoc.session import UserSession
from aoc.solver import Solutions
from aoc.utils import defaults, validate, BANNER


def parse_args():
    parser = argparse.ArgumentParser(prog='AoC pipeline', usage='%(prog)s year(s) day(s) part(s) [options]')
    parser.add_argument('-y', '--years', nargs='*', dest='years',
            default=defaults.YEARS, help='set what AoC years to solve problems from')
    parser.add_argument('-d', '--days', nargs='*', dest='days',
            default=defaults.DAYS, help='set what days to solve')
    parser.add_argument('-p', '--parts', nargs='*', dest='parts',
            default=defaults.PARTS, help='set what parts of a day to solve')
    parser.add_argument('-v', '--verbose', action='store_true',
            dest='verbose', help='set printing mode for solution times')
    args = parser.parse_args()
    return args

def validate_args(args):
    years = args.years
    days = args.days
    parts = args.parts
    verbose = args.verbose

    if not validate(years, 'y'):
        raise ValueError(
                f'years argument is not valid, {years=}')

    if not validate(days, 'd'):
        raise ValueError(
                f'days argument is not valid, {days=}')

    if not validate(parts, 'p'):
        raise ValueError(
                f'parts argument is not valid, {parts=}')

    return years, days, parts, verbose

if __name__ == '__main__':
    args = parse_args()
    years, days, parts, verbose = validate_args(args)
    solver = Solutions()
    user = UserSession(years, days, parts, solver)
    user.solve()
    if verbose:
        user.stats()

