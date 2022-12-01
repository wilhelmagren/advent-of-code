"""
MIT License

Copyright (c) 2022 Neurocode

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

File created: 2021-12-01
Last updated: 2022-12-01
"""
import time
import subprocess
import asyncio
import os
import sys
import numpy as np
from pathlib import Path
from collections import defaultdict
from adventofcode.datautil import request, get_filepaths
from adventofcode.utils import defaults, colours, printer, get_ydp

class Solver:
    def __init__(self, *args, **kwargs):
        self._setup(*args, **kwargs)
    
    def _setup(self, args, **kwargs):
        self.verbose = args['verbose']
        self.years = args['years']
        self.days = args['days']
        self.parts = args['parts']
        self.data_filepaths = list(item for sublist in get_filepaths(self.years, self.days, tpe='data') for item in sublist)
        self.solution_filepaths = get_filepaths(self.years, self.days, self.parts, tpe='solutions')
        self.results = dict()

    def run(self, log_success=False):
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
                    printer.ERROR(f'error caught when solving {year=} {day=} {part=}: {result.stderr}')
                else:
                    self.results[(year, day, part)] = result.stdout.split(' ')
        if log_success:
            printer.WORKING(f'done running your solutions! {len(self.results)} successful implementations.')

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
            print(f'  {year}-{int(day):02d}-{int(part)}    {answer}      {t_colour}{t_time}{precision}{colours.END}            {d_colour}{d_time}{precision}{colours.END}            {s_colour}{s_time}{precision}{colours.END}\n')

