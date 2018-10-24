import itertools

if __name__ == '__main__':
    for i in itertools.combinations([i for i in range(8)], 2):
        print(type(i))
        print(i[0])