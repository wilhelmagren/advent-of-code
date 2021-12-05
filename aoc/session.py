"""user session implementation for fetching, storing, and managing
the required user session token for curling respective problem input.

Authors: Wilhelm Ågren <wagren@kth.se>
Last edited: 03-12-2021
"""
import time
import os
import subprocess
import asyncio
import numpy as np

from collections import defaultdict
from .utils import get_session_token, split_problem, generator, Buffer, colors
from .utils import datafile_exists, get_datafiles, check_problems, format_problems


class UserSession:
    def __init__(self, years, days, parts, solver, *args, **kwargs):
        self.TOKEN = get_session_token()
        self.years = years
        self.days = days
        self.parts = parts
        self.results = defaultdict(list)
        self.solver = solver
        self.buffer = Buffer()
        self._setup()

    def _setup(self):
        self.problems = check_problems(format_problems(self.years, self.days, self.parts), self.solver)
        self.datafiles = get_datafiles(self.problems)

    def _generate(self, datafile, mode='r'):
        t_start = time.perf_counter_ns()
        data = list(generator(datafile, mode=mode))
        return data, time.perf_counter_ns() - t_start

    async def fetch_input(self, problem, print_output=False, sleep=2, **kwargs):
        year, day, _ = split_problem(problem)
        datadir = os.path.join(os.getcwd(), f'data/{year}/')
        if not os.path.isdir(datadir):
            self.buffer.write(f'[!]  no folder for {year=}, creating it...')
            os.mkdir(datadir)
        command = f"""curl https://adventofcode.com/{year}/day/{day}/input > data/{year}/d{day}.in -b session={self.TOKEN}"""
        status, curl_output = subprocess.getstatusoutput(command)
        await asyncio.sleep(sleep)  # advent-of-code author doesn't want too much traffic on his server, it is fragile...
        if status:
            raise ValueError(
                    'could not curl input for {year=} {day=}. subprocess response code {status=}')
        self.buffer.write(curl_output) if print_output else None

    def solve(self, problems=None, datafiles=None, print_progress=False):
        if problems is None:
            problems = self.problems
        if datafiles is None:
            datafiles = self.datafiles

        if not problems:
            self.buffer.write(f'{colors.BOLD}{colors.RED}[!]  no solution implementations found for the given problems{colors.END}')
            return

        for problem, datafile in zip(problems, datafiles):
            if not datafile_exists(problem):
                self.buffer.write(f'[!]  datafile for {problem=} doesn`t exist, fetching it...')
                asyncio.run(self.fetch_input(problem))
            self.buffer.write(f'[*]  solving {problem=}') if print_progress else None
            data, d_time = self._generate(datafile)
            answer, s_time = getattr(self.solver, problem)(data)
            self.results[problem.split('p')[0]].append((answer, d_time, s_time))
    
    def stats(self, decimals=3, padding=8):
        self.buffer.write(f'\n{colors.BOLD}   Problem           Answer           Total time          Data-io time          Solving time')
        self.buffer.write(f'==============================================================================================={colors.END}')
        for key, val in self.results.items():
            year, day = key.split('d')
            year = year[1:]
            for part, values in enumerate(val):
                answer, d_time, s_time = values
                self.buffer.write(f'')
                #self.buffer.write(f'\n{colors.BOLD}[*]  Answer to {year} day {int(day):02d} part {part+1}: {colors.BLUE}{answer}{colors.END}')
                #self.buffer.write(f'   total time      data-io time      solving time')
                #self.buffer.write(f'------------------------------------------------------{colors.END}')
                d_time_ms = np.round(d_time / 1_000_000, decimals).astype(float)
                s_time_ms = np.round(s_time / 1_000_000, decimals).astype(float)
                t_time_ms = np.round(d_time_ms + s_time_ms, decimals).astype(float)
                d_color, s_color, t_color = colors.GREEN, colors.GREEN, colors.GREEN
                
                # data-io time in ms
                if .5 <= d_time_ms < 1.:
                    d_color = colors.YELLOW
                elif 1. <= d_time_ms:
                    d_color = colors.RED
                
                # solution time in ms
                if 5. <= s_time_ms < 50.:
                    s_color = colors.YELLOW
                elif 50. <= s_time_ms:
                    s_color = colors.RED
                
                # total time in ms
                if 6. <= t_time_ms < 51.:
                    t_color = colors.YELLOW
                elif 51. <= t_time_ms:
                    t_color = colors.RED

                d_time_ms = f'{d_time_ms:.3f}'.center(padding)
                s_time_ms = f'{s_time_ms:.3f}'.center(padding)
                t_time_ms = f'{t_time_ms:.3f}'.center(padding)
                answer = f'{answer}'.center(padding+padding + 1)
                self.buffer.write(f'  {year}-{int(day):02d}-{part+1}    {answer}      {t_color}{t_time_ms}ms{colors.END}            {d_color}{d_time_ms}ms{colors.END}            {s_color}{s_time_ms}ms{colors.END}\n')




