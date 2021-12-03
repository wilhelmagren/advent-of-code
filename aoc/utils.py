"""utility function implementations for the AdventofCode (AoC) pipeline.
wow! take a look at that sexy banner, dont you want one as well?...
 - (https://patorjk.com/software/taag/#p=display&f=Slant&t=Advent%20of%20Code)

this file is a hot pile of garbage right now, but the functions gets the job done.
TODO: clean up some deprecated functions and look at adding some more times
        stats for each problem solution. make the code good...

Authors: Wilhelm Ågren <wagren@kth.se>
Last edited: 02-12-2021
"""
import os
import sys

from abc import ABC


class defaults(ABC):
    DAYS = list(range(1, 26))
    YEARS = list(range(2016, 2022))
    PARTS = list(range(1, 3))

class colors(ABC):
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    END = '\033[0m'
    BOLD = '\033[1m'

class Buffer(object):
    def __init__(self, *args, **kwargs):
        self.stdout = sys.stdout
        self._buff = ''

    def write(self, string):
        print(string)
        self.buff = self._buff.join(s for s in string)
        self.stdout.write(self._buff)
        self._buff = ''

    def put(self, string):
        self.buff = self._buff.join(s for s in string)


def find_session_token(*args, fname='session.token', **kwargs):
    """search through all subfolders in the directory for a file called
    `session.token` that contains the corresponding session token for the
    user. this token is to be used by the UserSession to curl missing
    data files.
    """
    cwd = os.getcwd()
    files = list(f for f in os.listdir(cwd))
    return os.path.join(cwd, fname) if fname in files else False

def get_session_token(*args, **kwargs):
    tokenpath = find_session_token()
    if not tokenpath:
        raise ValueError(
                'could not find a file named `session.token`, make sure to create one.')
    
    with open(tokenpath, 'r') as f:
        token = f.readline().rstrip()
        if not type(token) is str:
            raise ValueError(
                    'the stored session token is invalid, look over formatting.')
    return token

def datafile_exists(problem, *args, **kwargs):
    year, day, _ = split_problem(problem)
    cwd = os.getcwd()
    datadir = os.path.join(cwd, f'data/{year}/')
    for inputfile in os.listdir(datadir):
        if f'd{day}.in' == inputfile:
            return True
    return False

def split_problem(problem):
    splitted = problem.split('d')
    day, part = splitted[1].split('p')
    year = splitted[0][1:]
    return (year, day, part)

def validate(iterable, condition):
    mapping = {'y': defaults.YEARS, 'd': defaults.DAYS, 'p': defaults.PARTS}
    requirements = [
        all(list(map(lambda x: int(x) in mapping[condition], iterable))),
        len(iterable) <= len(mapping[condition])]
    return all(requirements)

def intify(iterable):
    return list(int(item) for item in iterable)

def exists(solutions, solution):
    return hasattr(solutions, solution)

def format_problems(years, days, parts):
    return list(f'f{year}d{day}p{part}' for year in years for day in days for part in parts)

def format_datafile(problem):
    year, day, _ = split_problem(problem)
    return f'data/{year}/d{day}.in'

def check_problems(problems, solutions):
    return list(problem for problem in problems if exists(solutions, problem))

def get_datafiles(problems):
    """get and format the datafiles
    """
    return list(format_datafile(problem) for problem in problems)

def generator(fname, mode='r'):
    """generate problem data from input file.
    yields a line from the file, if it exists.
    """
    with open(fname, mode) as f:
        for line in f.readlines():
            yield line.rstrip()


BANNER = f"""
{colors.BOLD}{colors.RED}
==========================================================================={colors.GREEN}
---------------------------------------------------------------------------{colors.END}
    ___       __                 __           ____   ______          __   
   /   | ____/ /   _____  ____  / /_   ____  / __/  / ____/___  ____/ /__ 
  / /| |/ __  / | / / _ \/ __ \/ __/  / __ \/ /_   / /   / __ \/ __  / _ \\
 / ___ / /_/ /| |/ /  __/ / / / /_   / /_/ / __/  / /___/ /_/ / /_/ /  __/
/_/  |_\__,_/ |___/\___/_/ /_/\__/   \____/_/     \____/\____/\__,_/\___/ 
{colors.GREEN}
---------------------------------------------------------------------------{colors.RED}
===========================================================================
{colors.END}
"""
