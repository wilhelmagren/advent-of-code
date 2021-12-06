"""
"""

import os
import sys

from .utils import printer, query_user, defaults, validfiles

def setup_paths(*args, **kwargs):
    """look for `data/`and `solutions/` directories in root,
    verify that they proclaim the specified structure:
    data:           <subdir>/<year>/d<day>.in
    solution:       <subdir>/<year>/d<day>p<part>.py

    function will handle missing directories and create them
    for the user. if all is setup already, let user know.

    also looks for required `session.token` file that includes
    the user cookie SESSION needed to curl input data for 
    respective missing day.
    """
    currpaths = os.listdir(os.getcwd())
    subdirs = ['data', 'solutions']
    exists = dict(data=False, solutions=False)
    for path in currpaths:
        for subdir in subdirs:
            if os.path.isdir(path) and path == subdir:
                exists[subdir] = True
                printer.WORKING(f'{subdir}/ directory already exists, do you want to verify its structure? [y/N]')
                response = query_user('N', 'y')
                if not response and subdir == 'data':
                    _verify_datadir(os.path.join(os.getcwd(), subdir), subdir)
                if not response and subdir == 'solutions':
                    _verify_solutiondir(os.path.join(os.getcwd(), subdir), subdir)
    for subdir, exist in exists.items():
        if not exist:
            printer.WORKING(f'{subdir}/ directory does not exist, I will set it up for you ...')
            _setup_directory(subdir)

def _setup_directory(subdir, *args, **kwargs):
    newdir = os.path.join(os.getcwd(), subdir)
    try:
        os.mkdir(newdir)
        for year in defaults.YEARS:
            os.mkdir(os.path.join(newdir, year))
        printer.WORKING(f'successfully created {subdir} directory')
    except ValueError:
        printer.ERROR(f'could not create {subdir} directory!')


def _verify_solutiondir(fullpath, subdir, *args, **kwargs):
    raise NotImplementedError('i have not done this yet')

def _verify_datadir(fullpath, subdir, *args, **kwargs):
    subdirpaths = os.listdir(os.path.join(fullpath))
    datafiles = dict(valid=list(), invalid=list())
    for path in subdirpaths:
        if path not in defaults.YEARS:
            printer.WARNING(f'found dir={path}/ in {subdir}/, pipeline expects no data to be located there ...')
        if path in defaults.YEARS:
            for possible_datafile in os.listdir(os.path.join(fullpath, path)):
                if possible_datafile not in validfiles.DATA:
                    printer.WARNING(f'datafile={possible_datafile} in {subdir}/{path} does not match naming convention ... ')
                    datafiles['invalid'].append(os.path.join(os.path.join(fullpath, path), possible_datafile))
                else:
                    datafiles['valid'].append(os.path.join(os.path.join(fullpath, path), possible_datafile))
    if len(datafiles['invalid']) == 0:
        printer.WORKING(f'you have no invalid datafiles and {len(datafiles["valid"])} valid datafile(s)')
    else:
        printer.WORKING(f'you have {len(datafiles["valid"])} valid datafile(s)')
        printer.WORKING(f'do you want me to try and automatically fix the {len(datafiles["invalid"])} invalid datafile(s)? [Y/n]')
        response = query_user('Y', 'n')
        if response:
            _format_datapaths(datafiles['invalid'])


def _format_datapaths(datafiles, *args, **kwargs):
    can_reformat = list(formatted for formatted in list(_try_reformat_path(path) for path in datafiles) if formatted)
    for (fullpath, newname) in can_reformat:
        splitted = fullpath.split('/')
        directory = '/'.join(splitted[:-1])
        printer.WORKING(f'renaming {splitted[-1]} => {newname} in directory {directory} ...')
        os.rename(fullpath, os.path.join(directory, newname))

    printer.WARNING(f'could not rename {len(datafiles) - len(can_reformat)} invalid datafile(s), please fix them manually ...')

def _try_reformat_datapath(path, *args, **kwargs):
    filename = path.split('/')[-1]
    try:
        name, ending = filename.split('.')
        for valid in validfiles.DATA:
            if name in valid:
                return (path, f'{name}.in')
    except ValueError:
        return None
        

def curl_inputdata(*args, **kwargs):
    raise NotImplementedError('not done yet')

