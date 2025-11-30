with open("data.txt", "r") as f:
    data = f.readlines()

sol = 0
for i, line in enumerate(data):
    line = line.strip()
    games = line.split(":")[1].split(";")

    max_red = 0
    max_green = 0
    max_blue = 0

    for game in games:
        xd = game.split(",")
        for xdd in xd:
            if "red" in xdd:
                max_red = max(max_red, int(xdd.split(" ")[1]))
            if "green" in xdd:
                max_green = max(max_green, int(xdd.split(" ")[1]))
            if "blue" in xdd:
                max_blue = max(max_blue, int(xdd.split(" ")[1]))

    sol += max_red * max_green * max_blue

print(sol)

