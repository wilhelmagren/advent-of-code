import re
from collections import defaultdict

with open("d3.data", "r") as f:
    data = f.read().strip().split("\n")

n_rows = len(data)
rowlen = len(data[0])
box = (-1, 0, 1)
solution = 0

def is_gear(c):
    return c == "*"

def is_symbol(c):
    return all((
        not c.isdigit(),
        c != ".",
    ))

gear_indices = defaultdict(list)

def search_box(num, lidx, st, ed):
    for i in box:
        for j in range(st - 1, ed + 1):
            if 0 <= lidx + i < n_rows:
                if 0 <= j < rowlen:
                    if is_gear(data[lidx + i][j]):
                        gear_indices[(lidx + i, j)].append(num)
                    if is_symbol(data[lidx + i][j]):
                        return num

    return 0

for i, line in enumerate(data):
    for digit in re.finditer(r"\d+", line):
        num = int(digit.group(0))
        st = digit.start()
        ed = digit.end()
        solution += search_box(num, i, st, ed)

print(solution)

part2 = 0
for gears in gear_indices.values():
    if len(gears) == 2:
        part2 += gears[0] * gears[1]

print(part2)

