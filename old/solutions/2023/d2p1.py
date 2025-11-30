with open("data.txt", "r") as f:
    data = f.readlines()

RED = 12
GREEN = 13
BLUE = 14

sol = 0
for i, line in enumerate(data):
    line = line.strip()
    games = line.split(":")[1].split(";")
    
    valid = True

    for game in games:
        if not valid:
            break
        
        sets = game.split(",")

        for sett in sets:
            if "red" in sett:
                n_red = int(sett.split(" ")[1])
                if n_red > RED:
                    valid = False
                    continue

            if "green" in sett:
                n_green = int(sett.split(" ")[1])
                if n_green > GREEN:
                    valid = False
                    continue

            if "blue" in sett:
                n_blue = int(sett.split(" ")[1])
                if n_blue > BLUE:
                    valid = False
                    continue
        
    if valid:
        sol += i + 1

print(sol)

