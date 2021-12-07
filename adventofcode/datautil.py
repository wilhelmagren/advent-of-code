"""docstring missing.

Authors: Wilhelm Ågren <wagren@kth.se>
Last edited: 07-12-2021
"""
import os
import asyncio

from pathlib import Path
from requests import get, HTTPError
from .utils import printer


async def request(year, day):
    """Try to send a http GET request to `https://adventofcode/` and download
    the input data for the specified problem. If there already exists a data
    file for the problem, let user know and don't request anything.
    If there is no prior datafile for the problem, asyncronously send the 
    GET request with together with the user cookie called `session.token`.
    This token is required since each datafile is different from user
    to user; also to access a puzzle input one has to be logged in on the
    website. If there is no user cookie, or no file `session.token`, then
    the function raises a `FileNotFoundError` letting the user know that 
    they have to set up the cookie. 

    There are ofcourse two parts for each problem, but they share the same
    input data, so if the user is missing the data for both solution
    year=2021,day=02,part=1 and part=2, only one request will be made for
    the year and day.

    Parameters
    ----------
    year : str
        Specifies what adventofcode year the problem is from.
    day : str
        The day to request problem input from.

    Returns
    -------
    None
        Function will not return anything, i.e. it will not attempt
        to read the donwloaded data file and return it's contents
        to the user. This is handled per each problem solution.
    """
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
    """Generate a list of all valid filepath names for the specified type.
    The valid types are either 'data' or 'solutions'. The splatted arg tuple
    is broadcasted into the specific years/days/parts based on the given type.
    
    Parameters
    ----------
    *args : (list, list) | (list, list, list)
        Either called with years, days, parts or years, days depending on the
        specified type. As mentioned, these are broadcasted on based on the type.
        The order is specific, can not be 
    tpe : str | None
        Either 'data' or 'solutions' are valid keyword arguments. Otherwise function
        raises a ValueError because of unknown type specifier.

    Returns
    -------
    list
        The cleaned version of the list containing all valid available filepaths.
    """
    if tpe == 'data':
        years, days = args
        return list(map(lambda x: [x, x], list(f'data/{year}/d{day}.in' for year in years for day in days)))
    elif tpe == 'solutions':
        years, days, parts = args
        return list(f'solutions/{year}/d{day}p{part}.py' for year in years for day in days for part in parts)
    printer.ERROR(f'unknown type specifier, {tpe=}')
    raise ValueError

def _clean_pathlist(lst, tpe):
    """Take a list and specifier for subdirectory and remove the files which are non-existant.
    Does not make sure that the contents of the files are valid, only cleans out the files
    that do not exists. Make sure your implementations are bugfree!

    Parameters
    ----------
    lst : list
        The iterable which holds the filepaths.
    tpe : str
        Subdirectory specifier.

    Returns
    -------
    list
        Returns the given list but cleaned. Function may raise a ValueError if the subdirectory
        specifier is not recognized.
    """
    if tpe == 'data':
        return list(filepath for filepath in lst if Path(Path(__file__).parent.parent, filepath).exists())
    elif tpe == 'solutions':
        return list(filepath for filepath in lst if Path(Path(__file__).parent.parent, filepath).exists())
    printer.ERROR(f'unknown type specifier, {tpe=}')
    raise ValueError

