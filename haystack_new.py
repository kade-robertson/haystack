def expand_map(m):
    largest = max(map(len, m))
    for i in xrange(len(m)):
        while len(m[i]) < largest:
            m[i] += [' ']
    return m

def main():
    pass

if __name__ == '__main__':
    main()
