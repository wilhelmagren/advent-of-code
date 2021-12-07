"""Varying functions for setting up required directory structure and 
file naming conventions for the adventofcode pipeline.
Any function starting with an underscore should be treated as a private function
and NOT be imported from any other modules inside the adventofcode package. 

Public functions of this module:
    $ find_sessiontoken(str)        =>  PosixPath | None
    $ setup_dirs()                  =>  None
    $ verify_dir(str)               =>  None
    $ reformat_paths(str, list)     =>  None

Private _utility functions:
    $ _setup_dir(str)               =>  None
    

Authors: Wilhelm Ågren <wagren@kth.se>
Last edited: 07-12-2021
"""
import os
import sys

from collections import defaultdict
from pathlib import Path
from .utils import printer, query_user, defaults, validfiles


def find_sessiontoken(*args, f_name='session.token', **kwargs):
    """Look for the `session.token` file in the root 
    of the adventofcode directory. The user has to create
    this file in order to be able to get the requested
    data files from http://adventofcode.com/

    Parameters
    ----------
    *args : tuple
        Any number of optional arguments, currently ignored.
    f_name : str
        The filename of which the session cookie is supposedly present in.
        Defaults to 'session.token' as per specified by the naming convention.
    **kargs : dict
        Any number of keyword arguments, currently ignored.

    Returns
    -------
    PosixPath | None
        Return the found session.token path as PosixPath if it exists, else None.
    """
    root = Path(__file__).parent.parent
    sessiontoken_path = Path(root, f_name)

    if sessiontoken_path.exists():
        return sessiontoken_path
    return None

def setup_dirs(*args, **kwargs):
    """Initialize setup for data/ and solutions/ subdirs of root.
    The respective setup is handled by _setup_dir which takes
    the directory in question and works on it.

    Parameters
    ----------
    *args : tuple
        Any number of optional arguments, currently ignored.
    **kwargs : dict
        Any number of keyword arguments, currently ignored.

    Returns
    -------
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

    Parameters
    ----------
    subdir_f : str
        Specifies what required directory to look for and setup, either 'data' or 'solutions'.
    *args : tuple
        Any number of optional arguments, currently ignored.
    **kwargs : dict
        Any number of keyword arguments, currently ignored.

    Returns
    -------
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
    """Take a subdirectory, either 'data' or 'solutions', and verify its structure and 
    look for files violating the naming convention. Store the invalid filenames, and
    query the user if they want the pipeline to try and automatically fix them.
    A valid subdirectory structure would only contain directories with name
    <year> from the set [2016, 2021], and these directories contain files
    according to the naming convention of the specified subdir.
    Datafiles should follow the naming convention 'd<day>.in' and solution
    files should be named 'd<day>p<part>.py' where day and part should be a valid
    literal, as specified in the utils file. 

    Parameters
    ----------
    subdir : str
        Specifier of what subdirectory to verify+validate.
    *args : tuple
        Any number of positional arguments, currently ignored.
    **kwargs : dict
        Any number of keyword arguments, currently ignored.

    Returns
    -------
    None
        Function does not return anything. Called functions may throw FileNotFoundError
        or ValueError exceptions, so possibly try and catch these.
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
                    printer.WARNING(f"{'/'.join(datafile.parts[-3:])} does not match the naming convention ...")
                    datafiles['invalid'].append(datafile)
                    continue
                datafiles['valid'].append(datafile)
    valid, invalid = map(lambda x: len(x), datafiles.values())
    printer.WORKING(f'in {subdir.parts[-1]} you have {valid} valid files, and {invalid} invalid files')
    if invalid != 0:
        response = query_user('Y', 'n', f'do you want to try and automatically rename invalid files to match naming convention? [Y/n]')
        if response:
            reformat_paths(subdir, datafiles['invalid'])

def reformat_paths(subdir, files2format, *args, **kwargs):
    """Take the specified subdirectory type /subdir/ and the files to format,
    try to find a compatible new name which follows the naming convention and
    is based on the old incorrect name. 

    For data files currently only implemented fix of name when file-ending is incorrect.
    E.g. the file 'd1.inn' would be renamed 'd1.in'.

    TODO: implement a nearest neighobur method of renaming incorrect solution names...

    Parameters
    ----------
    subdir : str
        The specifier of subdirectory to work on, either 'data' or 'solutions'.
    file2format : list | generator | iterator
        An iterable container holding the filenames to try and reformat according to naming convention.

    Returns
    -------
    None
        Function directly tries to rename the PosixPath of the incorrectly named filepaths.
        Ergo, it does not return anyting. Function will throw various exceptions if it tries
        to rename a file that does not exist or if the filename is so messed up that you can't
        split it into name.ending parts.
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
                    break
        except ValueError:
            printer.ERROR(f'can not rename {path} ...')
    for (path, n_file) in reformatted_paths:
        try:
            n_file = Path(path.parent, n_file)
            path.rename(n_file)
            printer.WORKING(f"renaming {'/'.join(path.parts[-3:])} => {'/'.join(n_file.parts[-3:])}")
        except FileNotFoundError:
            printer.ERROR(f'could not rename {path} to {n_file} ...')

