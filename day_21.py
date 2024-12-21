from functools import cache

from run_util import run_puzzle

NUMERICAL = {
    '7': (0, 0), '8': (1, 0), '9': (2, 0),
    '4': (0, 1), '5': (1, 1), '6': (2, 1),
    '1': (0, 2), '2': (1, 2), '3': (2, 2),
    None: (0, 3), '0': (1, 3), 'A': (2, 3)
}

DIRECTIONAL = {
    None: (0, 0), '^': (1, 0), 'A': (2, 0),
    '<': (0, 1), 'v': (1, 1), '>': (2, 1)
}


def parse_data(data):
    return data.strip().splitlines()


@cache
def path(start, end):
    pad = NUMERICAL if (start in NUMERICAL and end in NUMERICAL) else DIRECTIONAL

    (sx, sy) = pad[start]
    (ex, ey) = pad[end]

    dx = ex - sx
    dy = ey - sy

    y_moves = '^' * abs(dy) if dy < 0 else 'v' * dy
    x_moves = '<' * abs(dx) if dx < 0 else '>' * dx

    space_x, space_y = pad[None]
    bad_x, bad_y = (space_x - sx, space_y - sy)

    has_positive_dx = (dx > 0)
    bad_is_exact_dx = (bad_x == dx and bad_y == 0)
    bad_is_exact_dy = (bad_x == 0 and bad_y == dy)

    prefer_y_first = (has_positive_dx or bad_is_exact_dx) and not bad_is_exact_dy

    return (y_moves + x_moves if prefer_y_first else x_moves + y_moves) + "A"


@cache
def length(code, depth):
    if depth == 0:
        return len(code)

    s = 0
    for index, char in enumerate(code):
        s += length(path(code[index - 1], char), depth - 1)
    return s


def part_a(data):
    codes = parse_data(data)
    return sum(int(code[:-1]) * length(code, 3) for code in codes)


def part_b(data):
    codes = parse_data(data)
    return sum(int(code[:-1]) * length(code, 26) for code in codes)


def main():
    examples = [
        (
            """029A
980A
179A
456A
379A
""",
            126384,
            None
        )
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == "__main__":
    main()
