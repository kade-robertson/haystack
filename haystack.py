import sys

def plus_(s):  return s + [s.pop(-2) + s.pop()]
def minus_(s): return s + [s.pop(-2) - s.pop()]
def mult_(s):  return s + [s.pop(-2) * s.pop()]
def divd_(s):  return s + [float(s.pop(-2)) / float(s.pop())]
def input_(s): return s + [input()]
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
    print s[-1]
    return s
def outc_(s):
    print chr(s[-1])
    return s

def movement(char,x,y):
    if char == '>':   return x+1,y
    elif char == '<': return x-1,y
    elif char == '^': return x,y-1
    elif char == 'v': return x,y+1

def process(program):
    lines  = program.split('\n')
    matrix = [[[' '],[char for char in line]][line != ''] for line in lines]
    funcs = { '+': plus_,  '-': minus_, '*': mult_,  '/': divd_,
              'i': input_, 'o': outn_,  'c': outc_,  'd': dupl_,
              '@': rott_,  '[': lthan_, ']': gthan_, '=': eqto_,
              ',': disc_,  ';': swap_ }
    stack = []
    dx,dy = 1,0
    x,y   = 0,0
    strlt = ""
    isstr = False
    while matrix[y][x] != '|':
        char = matrix[y][x]
        if char in '<>^v' and not isstr:
            tx,ty = x,y
            x,y = movement(char,x,y)
            dx,dy = x-tx,y-ty
        elif char == '/':
            dx,dy = [dy == -1,-1][dy == 1],[dx == -1,-1][dx == 1]
            x,y = x+dx,y+dy
        elif char == '\\':
            dx,dy = [dy == 1,-1][dy == -1],[dx == 1,-1][dx == -1]
            x,y = x+dx,y+dy
        elif char in funcs and not isstr:
            stack = funcs[char](stack)
            x,y = x+dx,y+dy
        elif char in '0123456789':
            stack += [int(char)]
            x,y = x+dx,y+dy
        elif char == '?' and not isstr:
            cond = stack.pop()
            if dx != 0 and dy == 0:
                if cond:
                    dx,dy = 0,-1
                else:
                    dx,dy = 0,1
            elif dy != 0 and dx == 0:
                if cond:
                    dx,dy = 1,0
                else:
                    dx,dy = -1,0
            x,y = x+dx,y+dy
        elif char == '"':
            if isstr:
                stack += [strlt]
                strlt = ""
                isstr = False
            else:
                isstr = True
            x,y = x+dx,y+dy
        elif isstr:
            strlt += char
            x,y = x+dx,y+dy
        else:
            x,y = x+dx,y+dy
        y = y%len(matrix)
        x = x%len(matrix[y])

def main():
    if len(sys.argv) > 1:
        data = open(sys.argv[-1], 'r').read()
        if data == "":
            print "Where's the hay?"
        elif not '|' in data:
            print "Where's the needle?"
        else:
            process(data)
    else:
        print "Usage: %s <filename>" % (sys.argv[0].split('/')[-1])

if __name__ == '__main__':
    main()
