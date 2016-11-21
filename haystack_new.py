import os
import argparse

def expand_map(m):
    largest = max(map(len, m))
    for i in xrange(len(m)):
        while len(m[i]) < largest:
            m[i] += ' '
    return largest, len(m), m

def interpret(prog, debug):
    maxr, maxc, prog = expand_map(prog)
    stack = []
    dx, dy = 1, 0 # defaults to moving right
    x, y = 0, 0
    steps = 0
    while prog[x][y] != '|':
        steps += 1
        char = prog[x][y]
        if char == '>':
            dx, dy = 1, 0
        elif char == '<':
            dx, dy = -1, 0
        elif char == '^':
            dx, dy = 0, -1
        elif char == 'v':
            dx, dy = 0, 1
        elif char == '/':
            if dx == 1: dx, dy = 0, -1
            elif dx == -1: dx, dy = 0, 1
            elif dy == 1: dx, dy = -1, 0
            elif dy == -1: dx, dy = 1, 0
        elif char == '\\':
            if dx == 1: dx, dy = 0, 1
            elif dx == -1: dx, dy = 0, -1
            elif dy == 1: dx, dy = 1, 0
            elif dy == -1: dx, dy = -1, 0
        elif char == '?':
            if stack:
                cond = stack.pop()
                good, bad = (0, 0), (0, 0)
                if dx == 1: good, bad = (1, 0), (0, 1)
                elif dx == -1: good, bad = (-1, 0), (0, -1)
                elif dy == 1: good, bad = (0, 1), (1, 0)
                elif dy == -1: good, bad = (0, -1), (-1, 0)
                if cond:
                    dx, dy = good
                else:
                    dx, dy = bad
        x, y = x + dx, y + dy
        x = x % maxr
        y = y % maxc
    if debug:
        print('Steps made: %d'%steps)

def read_prog(path, debug = False):
    prog = ''
    with open(path, 'r') as file:
        prog = file.read()
    interpret(prog.split('\n'), debug)

def main():
    parser = argparse.ArgumentParser(description = 'Interpreter for the Haystack programming language.')
    parser.add_argument('-f', type=str, help='Open a Snake source file.')
    parser.add_argument('-d', action='store_true', help='Print debug information.')
    args = parser.parse_args()
    if args.f != None:
        if args.f != '':
            if os.path.isfile(args.f):
                read_prog(args.f, args.d)
            else:
                print('-f: Error - File path given does not exist.')
        else:
            print('-f: Error - no path given.')

if __name__ == '__main__':
    main()
