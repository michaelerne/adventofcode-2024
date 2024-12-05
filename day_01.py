from collections import Counter

from parse import findall

from run_util import run_puzzle


def parse_data(data):
    return zip(*findall('{:d}   {:d}', data))


def part_a(data):
    left, right = parse_data(data)

    return sum(
        abs(a - b)
        for a, b in zip(sorted(left), sorted(right))
    )


def part_b(data):
    left, right = parse_data(data)
    right_count = Counter(right)

    return sum(
        a * right_count[a]
        for a in left
    )


def main():
    examples = [
        ("""3   4
4   3
2   5
1   3
3   9
3   3
""", 11, 31)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
