"""Solver class implementation. It has three main methods which may be
invoked from the pipeline based on the CLI arguments. 

Public functions of the class:
    $ run(bool)                             =>  None
    $ answers(int | float)                  =>  None
    $ stats(int, int | float, str | char)   =>  None

The numpy dependency is questionable and it could have been implemented with 
the builtin math library, but I like the numpy API. Also, the asyncio 
import exists due to the potential asynchronuous behaviour of a http GET
request. The request module does not inheritely require this, but I decided
to wrap this to avoid any unwanted behaviour, .e.g requesting the same file
twice because a subprocess in the run function is done faster than the
GET request can be downloaded.

Authors: Wilhelm Ågren <wagren@kth.se>
Last edited: 08-12-2021
"""
import time
import subprocess
import asyncio
import os
import sys
import numpy as np

from pathlib import Path
from collections import defaultdict
from .datautil import request, get_filepaths
from .utils import defaults, colours, printer, get_ydp


class Solver:
    def __init__(self, *args, **kwargs):
        self._setup(*args, **kwargs)
    
    def _setup(self, args, **kwargs):
        """private setup function for the Solver class, called when __init__
        after __new__. Extracts the given arguments from the CLI and also
        generates valid data- and solution filepaths that is later iterated
        in the run method. Create an attribute dictionary which stores the
        stdout from the subprocess and later be used in the stats method.
        and indirectly expects it to be a string

        Parameters
        ----------
        args : dict
            Dictionary directly casted from the argparser Namespace, i.e it contains
            the specified CLI arguments. 
        """
        self.verbose = args['verbose']
        self.years = args['years']
        self.days = args['days']
        self.parts = args['parts']
        self.data_filepaths = list(item for sublist in get_filepaths(self.years, self.days, tpe='data') for item in sublist)
        self.solution_filepaths = get_filepaths(self.years, self.days, self.parts, tpe='solutions')
        self.results = dict()

    def run(self, log_success=False):
        """Run the solutions which the user specified from the CLI.
        If the user wants to solve something which does not exist, then
        simply skip trying to solve it - easy as that. The solutions are 
        expected to be stored in separate .py files that follow a somewhat
        specific template. This template can be found in the root directory 
        of this git repository. It needs to handle reading data from the 
        command line, i.e. sys.argv, also the convention of this pipeline
        is that each solution file prints to sys.stdout the: 1) answer,
        2) inpt data reading time, and 3) the time to calculate the answer.
        This write to stdout is captured by the subprocess library of python
        and we can access this and store it in the attribute dictionary
        .results for the initialized class. If the subprocess for some reason
        captures anything from stderr, then no results from stdout are saved 
        and the user is made aware that an error occured through the printer
        class. The results are stored in the attribute dictionary with keys
        (year, day, part) of the specific problem it solves, and result has
        to, as mentioned, be a string of the form '<answer> <io_time> <solution_time>.

        Parameters
        ----------
        log_success : bool
            Set whether or not to print how many subprocesses where successful when
            all solutions have been run. 

        """
        root = Path(__file__)
        printer.WORKING(f'running your solutions, this might take a while ...')
        for solution, datafile in zip(self.solution_filepaths, self.data_filepaths):
            datapath = Path(root.parent.parent, datafile)
            solutionpath = Path(root.parent.parent, solution)
            year, day, part = get_ydp(solutionpath)
            if solutionpath.exists():
                if not datapath.exists():
                    asyncio.run(request(year, day))
                result = subprocess.run(['python3', str(solutionpath), str(datapath)], capture_output=True, text=True)
                if result.stderr:
                    logger.ERROR(f'error caught when solving {year=} {day=} {part=}: {result.stderr}')
                else:
                    self.results[(year, day, part)] = result.stdout.split(' ')
        if log_success:
            printer.WORKING(f'done! {len(self.results)} successful implementations.')

    def answers(self, padding=8):
        """Print the collected answers for the solved solutions.
        Follows same template as when invoking `stats` in verbose 
        mode. TODO: implement more

        Parameters
        ----------
        padding : int | float
            The amount to pad the answer, on both sides.

        """
        print(f'\n{colours.BOLD}   Problem           Answer')
        print(f'==============================={colours.END}')
        for key, val in self.results.items():
            year, day, part = key
            answer, _, _ = val
            answer = f'{answer}'.center(padding+padding+1)
            print(f'  {year}-{int(day):02d}-{int(part)}    {answer}      ')


    def stats(self, decimals=2, padding=8, precision='ms'):
        """Printing collected answers and time stats for the
        solved solutions. 

        Parameters
        ----------
        decimals : int
            The amount of decimals to round to for each time.
        padding : int | float
            The amount to pad the answer and times, on both sides.
        precision : str | char
            The wanted precision for the time prints, either of 's', 'ms', 'us', 'ns'.

        """
        mapping = dict(s=1e9, ms=1e6, us=1e3, ns=1)
        print(f'\n{colours.BOLD}   Problem           Answer           Total time          Data-io time          Solving time')
        print(f'==============================================================================================={colours.END}')
        for key, val in self.results.items():
            year, day, part = key
            answer, io_time, solving_time = val
            d_time = np.round(int(io_time) / mapping[precision], decimals).astype(float)
            s_time = np.round(int(solving_time) / mapping[precision], decimals).astype(float)
            t_time = np.round(d_time+s_time, decimals).astype(float)
            d_colour, s_colour, t_colour = colours.GREEN, colours.GREEN, colours.GREEN
            
            if .5e6/mapping[precision] <= d_time < 1e6/mapping[precision]:
                d_colour = colours.YELLOW
            elif 1e6/mapping[precision] <= d_time:
                d_colour = colours.RED
            
            if 5e6/mapping[precision] <= s_time < 50e6/mapping[precision]:
                s_colour = colours.YELLOW
            elif 5e6/mapping[precision] <= s_time:
                s_colour = colours.RED

            if 6e6/mapping[precision] <= t_time < 51e6/mapping[precision]:
                t_colour = colours.YELLOW
            elif 51e6/mapping[precision] <= t_time:
                t_colour = colours.RED

            d_time = f'{d_time:.2f}'.center(padding)
            s_time = f'{s_time:.2f}'.center(padding)
            t_time = f'{t_time:.2f}'.center(padding)
            answer = f'{answer}'.center(padding+padding+1)
            print(f'  {year}-{int(day):02d}-{int(part)}    {answer}      {t_colour}{t_time}{precision}{colours.END}            {d_colour}{d_time}{precision}{colours.END}            {s_colour}{s_time}{precision}{colours.END}\n')

