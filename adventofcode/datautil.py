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
import os
import asyncio
from pathlib import Path
from requests import get, HTTPError
from .utils import printer


async def request(year, day):
    root = Path(__file__).parent.parent
    sessiontoken_path = Path(root, 'session.token')
    data_path = Path(root, 'data', year, f'd{day}.in')

    if data_path.exists():
        printer.WARNING(f'data file for {year=} {day=} already exists!')
        return
    data_path.touch()

    try:
        with open(sessiontoken_path) as f:
            cookie = dict(session=f.read().strip())
    except FileNotFoundError:
        printer.ERROR(f'no session token found in root directory ...')
        raise

    url = f'https://adventofcode.com/{year}/day/{day}/input'
    printer.WORKING(f'getting input file ...')
    response = get(url, cookies=cookie)

    try:
        response.raise_for_status()
    except HTTPError as e:
        printer.ERROR(f'something went wrong, trace: {e}')

    data = response.text.strip()
    with open(data_path, 'w') as f:
        for line in data:
            f.write(line)
        f.write('\n')
    printer.WORKING(f'done getting {year=} {day=} input file!')


def get_filepaths(*args, tpe=None):
    if tpe == 'data':
        years, days = args
        return list(map(lambda x: [x, x], list(f'data/{year}/d{day}.in' for year in years for day in days)))
    elif tpe == 'solutions':
        years, days, parts = args
        return list(f'solutions/{year}/d{day}p{part}.py' for year in years for day in days for part in parts)
    printer.ERROR(f'unknown type specifier, {tpe=}')
    raise ValueError

def _clean_pathlist(lst):
    return list(filepath for filepath in lst if Path(Path(__file__).parent.parent, filepath).exists())

