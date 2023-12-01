test1 = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
""".split("\n")

test2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
""".replace("one", "one1one").replace("two", "two2two") \
        .replace("three", "three3three").replace("four", "four4four").replace("five", "five5five") \
        .replace("six", "six6six").replace("seven", "seven7seven").replace("eight", "eight8eight") \
        .replace("nine", "nine9nine").split("\n")

with open("d1.data", "r") as f:
    lines = f.readlines()


lines = [l.strip().replace("one", "one1one").replace("two", "two2two") \
        .replace("three", "three3three").replace("four", "four4four").replace("five", "five5five") \
        .replace("six", "six6six").replace("seven", "seven7seven").replace("eight", "eight8eight") \
        .replace("nine", "nine9nine") for l in lines]
"""
lines = [l.strip() for l in lines]

"""

def str_or_digit(line):
    xdd = ''.join(filter(str.isdigit, line))
    print(line)

    if len(xdd):
        num = xdd[0] + xdd[-1]
    else:
        num = 0

    print(xdd, num)

    return int(num)

numsss = sum(map(str_or_digit, lines))
print(numsss)
