import os
import argparse

def plus_(s):  return s + [s.pop(-2) + s.pop()]
def minus_(s): return s + [s.pop(-2) - s.pop()]
def mult_(s):  return s + [s.pop(-2) * s.pop()]
def divd_(s):  return s + [s.pop(-2) / s.pop()]
def input_(s): return s + [eval(input())]
def rinp_(s):  return s + [input()]
def dupl_(s):  return s + [s[-1]]
def rott_(s):  return [s.pop()] + s
def gthan_(s): return s + [s.pop(-2) > s.pop()]
def lthan_(s): return s + [s.pop(-2) < s.pop()]
def eqto_(s):  return s + [s.pop(-2) == s.pop()]

def swap_(s):
    a = s.pop()
    b = s.pop()
    return s + [a] + [b]
def disc_(s):
    s.pop()
    return s
def outn_(s):
    print(s[-1])
    return s
def outc_(s):
    print(chr(s[-1]))
    return s

def expand_map(m):
    largest = max(map(len, m))
    for i in range(len(m)):
        while len(m[i]) < largest:
            m[i] += ' '
    return largest, len(m), m

def interpret(prog, debug, vdebug):
    maxr, maxc, prog = expand_map(prog)
    stack = []
    funcs = { '+': plus_,  '-': minus_, '*': mult_,  'D': divd_,
              'i': input_, 'o': outn_,  'c': outc_,  'd': dupl_,
              '@': rott_,  '[': lthan_, ']': gthan_, '=': eqto_,
              ',': disc_,  ';': swap_,  'I': rinp_ }
    dx, dy = 1, 0 # defaults to moving right
    x, y = 0, 0
    steps = 0
    while prog[y][x] != '|':
        steps += 1
        char = prog[y][x]
        if vdebug:
            print('Char: %s | Stack Before: %s'%(char, stack))
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
        elif char in '0123456789':
            numstr = ''
            while prog[y][x] in '0123456789':
                numstr += prog[y][x]
                x, y = x + dx, y + dy
                x = x % maxr
                y = y % maxc
            stack.append(int(numstr))
            x, y = x - dx, y - dy
            x = x % maxr
            y = y % maxc
        elif char in funcs:
            stack = funcs[char](stack)
        x, y = x + dx, y + dy
        x = x % maxr
        y = y % maxc
    if debug or vdebug:
        print('Steps made: %d'%steps)

def read_prog(path, debug, vdebug):
    prog = ''
    with open(path, 'r') as file:
        prog = file.read()
    interpret(prog.split('\n'), debug, vdebug)

def main():
    parser = argparse.ArgumentParser(description = 'Interpreter for the Haystack programming language.')
    parser.add_argument('-f', type=str, help='Open a Snake source file.')
    parser.add_argument('-d', action='store_true', help='Print debug information.')
    parser.add_argument('-D', action='store_true', help='Print detailed debug information.')
    args = parser.parse_args()
    if args.f != None:
        if args.f != '':
            if os.path.isfile(args.f):
                read_prog(args.f, args.d, args.D)
            else:
                print('-f: Error - File path given does not exist.')
        else:
            print('-f: Error - no path given.')

if __name__ == '__main__':
    main()
