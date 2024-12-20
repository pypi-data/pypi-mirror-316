import ujson


def append_text(filename: str, text: str) -> None:
    with open(filename, 'a') as file:
        file.write(text + '\n')


def draw_diagnal(filename: str, n: int):
    with open(filename, 'w') as file:
        for i in range(n - 1):
            print(i * ' ' + str(i + 1), file=file)
        i += 1
        print(i * ' ' + str(i + 1), file=file, end='')


def draw_square(filename: str, n: int):
    with open(filename, 'w') as file:
        print('*' * n, file=file)
        print((n - 2) * ('*' + (n - 2) * ' ' + '*\n'), file=file, end='')
        print('*' * n, file=file, end='')


def draw_triangle(filename: str, n: int):
    '''
    n must be positive integer.
    :param filename:
    :param n positive number:
    '''
    with open(filename, 'w') as file:
        print('*', file=file)
        for i in range(n - 1):
            print('*' + i * ' ' + '*', file=file)
        for i in range(n):
            print('*' + (n - 1 - i) * ' ' + '*', file=file)
        print('*', file=file, end='')


def write_json(filename: str, data: dict) -> None:
    with open(filename, 'w') as file:
        ujson.dump(data, file, indent=4)

    print('Write successfully!')
