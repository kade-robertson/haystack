import os
import math
import argparse
import itertools

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
def addau_(s): return s + ['ABCDEFGHIJKLMNOPQRSTUVWXYZ']
def addal_(s): return s + ['abcdefghijklmnopqrstuvwxyz']
def bin_(s):   return s + [bin(s.pop())[2:]]
def ubin_(s):  return s + [int(s.pop(), 2)]
def min_(s):   return s + [min(s.pop())]
def max_(s):   return s + [max(s.pop())]
def enum_(s):  return s + [[(x,y)for x,y in enumerate(s.pop())]]
def denum_(s): return s + [[x[1]for x in sorted(s.pop())]]
def zip_(s):   return s + [list(zip(s.pop(-2), s.pop()))]
def zipl_(s):  return s + [list(itertools.zip_longest(s.pop(-2), s.pop()))]
def rang_(s):  return s + [list(range(s.pop()))]
def irang_(s): return s + [list(range(1, s.pop()+1))]
def fact_(s):  return s + [math.factorial(s.pop())]

def uconf_(s):
    l = s.pop()
    return s + [l[1:],l[0]]
def uconb_(s):
    l = s.pop()
    return s + [l[:-1],l[-1]]
def fib_(s):
    n = s.pop()
    a, b = 0, 1
    while n:
        a, b = b, a+b
        n -= 1
    return s + [a]
def swap_(s):
    a = s.pop()
    b = s.pop()
    return s + [a] + [b]
def disc_(s):
    s.pop()
    return s
def out_(s):
    print(s[-1],end='')
    return s
def outnl_(s):
    print(s[-1],end='\n')
    return s
def outc_(s):
    print(chr(s[-1]),end='')
    return s
def outcnl_(s):
    print(chr(s[-1]),end='\n')
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
    funcs = { '+': plus_,   '-': minus_, '*': mult_,  'D': divd_,
              'i': input_,  'o': out_,   'c': outc_,  'd': dupl_,
              '@': rott_,   'l': lthan_, 'L': gthan_, '=': eqto_,
              ',': disc_,   ';': swap_,  'I': rinp_,  'O': outnl_,
              'C': outcnl_, 'a': addal_, 'A': addau_, 'b': bin_,
              'B': ubin_,   'm': min_,   'M': max_,   'e': enum_,
              'E': denum_,  'z': zip_,   'Z': zipl_,  'r': rang_,
              'R': irang_,  'f': fact_,  'F': fib_,   'u': uconf_,
              'U': uconb_ }
    dx, dy = 1, 0 # defaults to moving right
    x, y = 0, 0
    steps = 0
    while prog[y][x] != '|':
        steps += 1
        char = prog[y][x]
        if vdebug:
            direc = [[['up','down'][dy == 1],'left'][dx == -1],'right'][dx == 1]
            print('Char: %s | Posn: (%d, %d) going %s | Stack Before: %s'%(char, x, y, direc, stack))
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
        elif char == '"':
            sstr = ''
            x, y = x + dx, y + dy
            x = x % maxr
            y = y % maxc
            while prog[y][x] != '"':
                sstr += prog[y][x]
                x, y = x + dx, y + dy
                x = x % maxr
                y = y % maxc
            stack.append(sstr)
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
