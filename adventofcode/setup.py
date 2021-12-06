"""Varying functions for setting up required directory structure and 
file naming conventions for the adventofcode pipeline.
The main four functions to be called from a user created script are:
    1. find_sessiontoken
    2. setup_dirs
    3. verify_dir
    4. reformat_paths

The rest of the functions implemented in this file are to be trated as
private, hence the _ before the declared function name. They are utility 
functions used by the aforementioned public functions. 

Authors: Wilhelm Ågren <wagren@kth.se>
Last edited: 06-12-2021
"""
import os
import sys

from collections import defaultdict
from pathlib import Path
from .utils import printer, query_user, defaults, validfiles


def find_sessiontoken(*args, **kwargs):
    """Look for the `session.token` file in the root 
    of the adventofcode directory. The user has to create
    this file in order to be able to get the requested
    data files from http://adventofcode.com/

    Parameters:
    -----------
    *args : tuple
        Any number of optional arguments, currently ignored.
    **kargs : dict
        Any number of keyword arguments, currently ignored.

    Returns:
    --------
    PosixPath | None
        Return the found session.token path as PosixPath if it exists, else None.
    """
    root = Path(__file__).parent.parent
    sessiontoken_path = Path(root, 'session.token')

    if sessiontoken_path.exists():
        return sessiontoken_path
    return None

def setup_dirs(*args, **kwargs):
    """Initialize setup for data/ and solutions/ subdirs of root.
    The respective setup is handled by _setup_dir which takes
    the directory in question and works on it.

    Parameters:
    -----------
    *args : tuple
        Any number of optional arguments, currently ignored.
    **kwargs : dict
        Any number of keyword arguments, currently ignored.

    Returns:
    --------
    None
        Function does not return anything.
    """
    for subdir in ['data', 'solutions']:
        _setup_dir(subdir)

def _setup_dir(subdir_f, *args, **kwargs):
    """Work on setting up the specified subdir of root.
    Function looks through the root directory of the python project,
    tries to identify a PosixPath that is a directory and shares the 
    name of the given arguments, queries the user to verify the
    integrity of the directory if it exsists, otherwise create the
    necessary directories.

    Parameters:
    -----------
    subdir_f : str
        Specifies what required directory to look for and setup, either 'data' or 'solutions'.
    *args : tuple
        Any number of optional arguments, currently ignored.
    **kwargs : dict
        Any number of keyword arguments, currently ignored.

    Returns:
    --------
    None
        Function does not return anything.
    """
    root = Path(__file__).parent.parent
    subdir = Path(root, subdir_f)
    if subdir.exists():
        response = query_user('N', 'y', f'{subdir_f}/ already exists, do you want to verify its structure? [y/N]')
        if not response: verify_dir(subdir)
        return  # the specified directory exists and potentially have been verified, nothing else to do

    printer.WORKING(f'{subdir_f}/ directory does not exist, setting it up for you ...')
    subdir.mkdir()
    for year in defaults.YEARS:
        subsubdir = Path(subdir, year)
        if not subsubdir.exists():
            subsubdir.mkdir()
    printer.WORKING(f'done setting up {subdir_f}/ directory structure!')

def verify_dir(subdir, *args, **kwargs):
    """docstring missing.
    """
    root = Path(__file__).parent.parent
    subdir = Path(root, subdir)
    datafiles = dict(valid=list(), invalid=list())
    for child in subdir.iterdir():
        inner_dir = child.parts[-1]
        if inner_dir not in defaults.YEARS:
            printer.WARNING(f'directory {child} will be ignored by solver ...')
        else:
            for datafile in child.iterdir():
                if not any(datafile.parts[-1] in valid for valid in [validfiles.DATA, validfiles.SOLUTION]):
                    printer.WARNING(f'{datafile} does not match the naming convention ...')
                    datafiles['invalid'].append(datafile)
                    continue
                datafiles['valid'].append(datafile)
    valid, invalid = map(lambda x: len(x), datafiles.values())
    printer.WORKING(f'in {subdir} you have {valid} valid file(s), and {invalid} invalid file(s)')
    if invalid != 0:
        response = query_user('Y', 'n', f'do you want to try and automatically rename invalid files to match naming convention? [Y/n]')
        if response:
            reformat_paths(subdir, datafiles['invalid'])

def reformat_paths(subdir, files2format, *args, **kwargs):
    """docstring missing.
    """
    reformatted_paths = list()
    f_ending_fix = '.in' if subdir.parts[-1] == 'data' else '.py'
    validfiles_fix = validfiles.DATA if subdir.parts[-1] == 'data' else validfiles.SOLUTION
    for path in files2format:
        try:
            f_name, f_ending = path.parts[-1].split('.')
            for valid in validfiles_fix:
                if f_name in valid:
                    reformatted_paths.append((path, f'{f_name}{f_ending_fix}'))
        except ValueError:
            printer.ERROR(f'can not rename {path} ...')

    for (path, n_file) in reformatted_paths:
        print(path, n_file)
        try:
            n_file = Path(path.parent, n_file)
            path.rename(n_file)
            printer.WORKING(f'renaming {path.parts[-1]} => {n_file}')
        except ValueError:
            printer.ERROR(f'could not rename {path} to {n_file} ...')

