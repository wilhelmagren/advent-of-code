# Python Advent-of-Code package 🎄 🌟
This repository contains code for a Python module that enables streamlined
loading, solving, and answering of the `Advent of Code (AoC)` christmas
questions. It is written with the intention of offering the end user more
insight into memory usage, time complexity etc. for their provided solutions to
the AoC questions. Currently it only supports solutions written in Python but
allowing the user to answer in e.g. C, C++, Rust, etc. is a future feature that
I am looking into.

If you find any bug or have any suggestions on how to improve this package, go
down to the contact section to see full contribution guidelines [WIP].

## Directory setup
To run the streamlined pipeline it requires a specific directory structure. All data files should follow the naming convention of `d<day>.in` and be placed in `data/<year>/`. All solutions should follow the naming convention `d<day>p<part>.py` and be placed in `solutions/<year>/`. The package has a module for setting up the required directory structure automatically, but if you want to manually transfer files/solutions, make sure that your directory looks accordingly:
```
your-repository/
├── adventofcode/
│   ├── __init__.py
|   ├── datautil.py
|   ├── setup.py
│   ├── solver.py
│   └── utils.py
├── data/
│   ├── 2020/
|   |   └── ...
│   └── 2021/
|       ├── d1.in
|       ├── d2.in
|       └── ...
├── solutions/
│   ├── 2020/
|   |   └── ...
│   └── 2021/
|       ├── d1p1.py
|       ├── d1p2.py
|       ├── d2p1.py
|       └── ...
├── aoc.py
└── session.token
```
The `session.token` file is required so that you can autoamtically get the input file for the problem which you are trying to solve, if it already doesn't exist. It should contain one line with your user session cookie. This can be found if you inspect the network packages when accessing this [link](https://adventofcode.com/2021/day/3/input) whilst logged in to the website. 

## How to run
All solution implementation files should also follow a specific form. An example can be found in the `template-solution.py` file. Running the pipeline is as easy as invoking the file `aoc.py` with arguments specifying what you want to do. For example if you want to run your solutions for day 1 of 2021 AoC, run `python aoc.py --years 2021 --day 1 --parts 1 2 --verbose --run`. If you haven't manually downloaded the input files for those solutions, don't worry- the package will do that for you! All available arguments can be seen below:
```
usage: python aoc.py [-h] [-v] [-s] [-r] [-y [YEARS ...]] [-d [DAYS ...]] [-p [PARTS ...]]

Streamlined Advent of Code pipeline so that you can help save christmas as easily as possible!

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         print time-stats for your solutions
  -s, --setup           setup the required directory structures
  -r, --run             run the solver on your solutions
  -y [YEARS ...], --years [YEARS ...]
                        set what years to solve problems from
  -d [DAYS ...], --days [DAYS ...]
                        set what days to solve
  -p [PARTS ...], --parts [PARTS ...]
                        set what parts of a day to solve

We have to save christmas!
```

## Contact and license
TODO: WRITE CONTRIBUTION GUIDELINES
<br>Author: Wilhelm Ågren, wilhelmagren98@gmail.com
<br>All code is under an Apache-2.0 styled license, please see
[LICENSE](https://github.com/willeagren/advent-of-code/blob/rewrite-complete/LICENSE)
