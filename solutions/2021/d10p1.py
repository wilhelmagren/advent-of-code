"""Template for the adventofcode package pipeline.
Replace answer=None with your solution.
"""
import time
import sys
import fileinput as fi

def run(data, io_time):
    t_start = time.perf_counter_ns()
    scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
    openings = ['(', '[', '{', '<']
    c2o = {')':'(', ']':'[', '}':'{','>':'<'}
    illegals = []
    for line in data:
        openingstack = []
        for char in line:
            if char not in openings:
                if openingstack[-1] != c2o[char]:
                    illegals.append(char)
                    break
                else:
                    openingstack.pop()
            else:
                # opening new chunk
                openingstack.append(char)
    answer = sum(map(lambda x: scores[x], illegals))
    t_end = time.perf_counter_ns()
    sys.stdout.write(f'{answer} {io_time} {t_end-t_start}')

if __name__ == '__main__':
    t_start = time.perf_counter_ns()
    data = list(line.rstrip() for line in fi.input())
    #data = "[({(<(())[]>[[{[]{<()<>>\n[(()[<>])]({[<{<<[]>>(\n{([(<{}[<>[]}>{[]{[(<()>\n(((({<>}<{<{<>}{[]{[]{}\n[[<[([]))<([[{}[[()]]]\n[{[{({}]{}}([{[{{{}}([]\n{<[[]]>}<{[{[{[]{()[[[]\n[<(<(<(<{}))><([]([]()\n<{([([[(<>()){}]>(<<{{\n<{([{{}}[<[[[<>{}]]]>[]]".split('\n')
    #data = "{([(<{}[<>[]}>{[]{[(<()>\n(((({<>}<{<{<>}{[]{[]{}".split('\n')
    t_stop = time.perf_counter_ns()
    run(data, t_stop-t_start)

