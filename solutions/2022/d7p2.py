"""
Part 1.

Last edited: 2022-12-07
"""
import time
import sys
import fileinput as fi

class Dir:
    def __init__(self, parent, name):
        self._parent = parent
        self._name = name
        self._files = []
        self._children = {'..': parent}
        self._size = 0
    
    def move(self, loc):
        return self._children.get(loc, None)
    
    def file_sizes(self):
        return sum([file.size() for file in self._files])
    
    def size_of_dir(self):
        self._size += self.file_sizes()
        children = self._children.copy()
        del children['..']
        self._size += sum([child.size_of_dir() for child in children.values()])
        return self._size
    
    def add_children(self, rows):
        i = 0
        row = rows[i]
        while row[0] != '$':
            if _is_dir(row):
                name = _get_dir_name(row)
                self._children[name] = Dir(self, name)
            else:
                size, name = _get_file_props(row)
                size = int(size)
                self._files.append(File(self, size, name))
            i += 1
            if i >= len(rows):
                break
            row = rows[i]
    
    def get_all_dirs(self):
        dirs = [self]
        children = self._children.copy()
        del children['..']
        dirs.extend([child.get_all_dirs() for child in children.values()])
        return dirs

class File:
    def __init__(self, parent, size, name):
        self._parent = parent
        self._children = None
        self._size = size
        self._name = name
    
    def size(self):
        return self._size

def _get_file_props(row):
    return row.split(' ')
    
def _get_dir_name(row):
    return row.split(' ')[1]

def _is_dir(row):
    return True if row.split(' ')[0] == 'dir' else False

def _is_command(row):
    return True if row[0] == '$' else False

def _get_command(row):
    return row.split(' ')[1]

def _get_loc(row):
    return row.split(' ')[2]

def flatten(l):
    if l == []: return l
    if isinstance(l[0], list): return flatten(l[0]) + flatten(l[1:])
    return l[:1] + flatten(l[1:])

def run(data, io_time):
    t_start = time.perf_counter_ns()

    rootdir = Dir(None, '/')
    currdir = rootdir

    for i, row in enumerate(data):
        if _is_command(row):
            command = _get_command(row)
            if command == 'cd':
                loc = _get_loc(row)
                if loc == '/':
                    continue
                currdir = currdir.move(loc) 
            if command == 'ls':
                currdir.add_children(data[(i+1):])
    
    rootdir.size_of_dir()
    sizes = sorted([dir._size for dir in flatten(rootdir.get_all_dirs())])
    biggest = sizes[-1]
    unused = 70_000_000 - biggest
    for size in sizes:
        if  unused + size >= 30_000_000:
            sizes = size
            break

    answer = sizes

    t_stop = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_stop-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = list(line.rstrip() for line in fi.input())
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)
