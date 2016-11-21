def expand_map(m):
    largest = max(map(len, m))
    for i in xrange(len(m)):
        while len(m[i]) < largest:
            m[i] += [' ']
    return largest, len(m), m

def main(prog):
    maxr, maxc, prog = expand_map(prog)
    dx, dy = 1, 0 # defaults to moving right
    x, y = 0, 0
    while prog[x][y] != '|':
        char = prog[x][y]
        if char == '>':
            dx, dy = 1, 0
        elif char == '<':
            dx, dy = -1, 0
        elif char == '^':
            dx, dy = 0, 1
        elif char == 'v':
            dx, dy = 0, -1
        x, y = x + dx, y + dy
        x = x % maxr
        y = y % maxc

if __name__ == '__main__':
    main()
