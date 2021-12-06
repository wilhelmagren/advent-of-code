import os

from pathlib import Path
from requests import get, HTTPError
from .utils import printer


def request(year, day):
    root = Path(__file__).parent.parent
    sessiontoken_path = Path(root, 'session.token')
    data_path = Path(root, 'data', year, f'd{day}.in')

    if data_path.exists():
        printer.WARNING(f'data file for {year=} {day=} already exists!')
        return
    else:
        printer.WORKING(f'requested data file for {year=} {day=} doesn`t exists, touching it ...')
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

    printer.WORKING(f'writing input contents to {data_path} ...')
    data = response.text.strip()
    with open(data_path, 'w') as f:
        for line in data:
            f.write(line)
        f.write('\n')
    printer.WORKING(f'done getting {year=} {day=} input file!')

