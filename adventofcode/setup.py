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
import sys
from .utils import printer, query_user, defaults, validfiles
from pathlib import Path
from collections import defaultdict

__all__ = (
    'find_sessiontoken',
    'setup_dirs',
    'verify_dirs',
    'reformat_paths',
)

def find_sessiontoken(*args, f_name='session.token', **kwargs):
    root = Path(__file__).parent.parent
    sessiontoken_path = Path(root, f_name)

    if sessiontoken_path.exists():
        return sessiontoken_path
    return None

def setup_dirs(*args, **kwargs):
    for subdir in ['data', 'solutions']:
        _setup_dir(subdir)

def _setup_dir(subdir_f, *args, **kwargs):
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

