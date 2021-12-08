"""docstring missing.

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
        of the form `<answer> <io_time> <solution_time>`. If the subprocess
        captures anything from stderr then no result is stored and an error
        """
        self.verbose = args['verbose']
        self.years = args['years']
        self.days = args['days']
        self.parts = args['parts']
        self.data_filepaths = list(item for sublist in get_filepaths(self.years, self.days, tpe='data') for item in sublist)
        self.solution_filepaths = get_filepaths(self.years, self.days, self.parts, tpe='solutions')
        self.results = dict()

    def run(self, log_success=False):
        """docstring missing.
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
        print(f'\n{colours.BOLD}   Problem           Answer')
        print(f'==============================={colours.END}')
        for key, val in self.results.items():
            year, day, part = key
            answer, _, _ = val
            answer = f'{answer}'.center(padding+padding+1)
            print(f'  {year}-{int(day):02d}-{int(part)}    {answer}      ')


    def stats(self, decimals=2, padding=8, precision='ms'):
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
            print(f'  {year}-{int(day):02d}-{int(part)}    {answer}      {t_colour}{t_time}ms{colours.END}            {d_colour}{d_time}ms{colours.END}            {s_colour}{s_time}ms{colours.END}\n')

