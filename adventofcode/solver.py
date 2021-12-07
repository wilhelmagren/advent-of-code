"""docstring missing.

Authors: Wilhelm Ågren <wagren@kth.se>
Last edited: 07-12-2021
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
        """docstring missing.
        """
        self.verbose = args['verbose']
        self.years = args['years']
        self.days = args['days']
        self.parts = args['parts']
        self.data_filepaths = list(item for sublist in get_filepaths(self.years, self.days, tpe='data') for item in sublist)
        self.solution_filepaths = get_filepaths(self.years, self.days, self.parts, tpe='solutions')
        self.results = dict()

    def run(self, *args, **kwargs):
        """docstring missing.
        """
        root = Path(__file__)
        for solution, datafile in zip(self.solution_filepaths, self.data_filepaths):
            datapath = Path(root.parent.parent, datafile)
            solutionpath = Path(root.parent.parent, solution)
            year, day, part = get_ydp(solutionpath)
            if solutionpath.exists():
                if not datapath.exists():
                    asyncio.run(request(year, day))
                result = subprocess.run(['python3', str(solutionpath), str(datapath)], capture_output=True, text=True)
                if result.stderr:
                    print(result.stderr)
                self.results[(year, day, part)] = result.stdout.split(' ')

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















