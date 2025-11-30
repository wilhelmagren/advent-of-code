with open("d4p1.txt", "r") as f:
    data = f.read().strip().split("\n")

data = [l.replace(f"Card {i + 1}:", "") for i, l in enumerate(data)]
data = [l.split("|") for l in data]
winning = [l[0].split(" ") for l in data]
cards = [l[1].split(" ") for l in data]

winning = [list(filter(lambda s: s != "", l)) for l in winning]
cards = [list(filter(lambda s: s != "", l)) for l in cards]

mywin = []
for c, w in zip(cards, winning):
    mywin.append([])
    for n in w:
        if n in c:
            mywin[-1].append(w)

solution = 0
for w in mywin:
    numwin = len(w)
    if numwin > 0:
        solution += 2 ** (numwin - 1)

print(solution)

from collections import defaultdict

winnings = defaultdict(int)

for i, (c, w) in enumerate(zip(cards, winning)):
    ii = i + 1
    winnings[ii] += 1 
    num_match = len(set(c) & set(w))
    for nn in range(ii + 1, num_match + ii + 1):
        winnings[nn] += winnings[ii]

print(sum(winnings.values()))
