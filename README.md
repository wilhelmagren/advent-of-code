# Advent-of-Code Python package
Merry christmas and happy star hunting! :christmas_tree: :santa:

## Directory setup
This repo contains a template for AoC w/ **Python 3.8+** and my personal solutions for the 2021 problems. It is implemented using mostly built in libraries, except for the [numpy](https://numpy.org/) requirement. To run the pipeline it requires a specific directory structure. Make sure that your data files are stored accordingly:
```
advent-of-code/
├── aoc/
│   ├── __init__.py
|   ├── session.py
│   ├── solver.py
│   └── utils.py
├── data/
│   ├── 2019/
|   |   └── ...
│   ├── 2020/
|   |   └── ...
│   └── 2021/
|       ├── d1.in
|       ├── d2.in
|       └── ...
├── run.py
└── session.token
```

All solutions are to be implemented as a function with a specific name in the Solutions class found in the file ```solver.py```. The formatting of the function name should be of the form ```f<YEAR>d<DAY>p<PART>```, where the variables in ```<>```specifies the year, day, and part of a problem that the function solves. To run the advent-of-code pipeline you may run the script ```run.py``` with either no arguments to show all your implemented solutions, or specify year-day-part of what problems to solve:
```
usage: python3 run.py [options]

optional arguments:
  -h, --help            show this help message and exit
  -y [YEARS [YEARS ...]], --years [YEARS [YEARS ...]]
                        set what AoC years to solve problems from
  -d [DAYS [DAYS ...]], --days [DAYS [DAYS ...]]
                        set what days to solve
  -p [PARTS [PARTS ...]], --parts [PARTS [PARTS ...]]
                        set what parts of a day to solve
  -v, --verbose         set printing mode for solution times
  -b, --banner          print AoC banner at pipeline start
```

## Contact and license
If you have any suggestions on how to improve this pipeline, contact me or create a pull request!
<br>Author: Wilhelm Ågren, wagren@kth.se
<br>License: GNU General Public License v3.0
