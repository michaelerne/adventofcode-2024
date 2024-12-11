from collections import defaultdict
from math import log10

from run_util import run_puzzle


def parse_data(data):
    stones = list(map(int, data.split()))
    counts = defaultdict(int)
    for stone in stones:
        counts[stone] += 1
    return counts


def blink(counts, cache):
    new_counts = defaultdict(int)
    for stone, count in counts.items():
        if stone == 0:
            new_counts[1] += count
        else:
            length = int(log10(stone)) + 1
            if length % 2 == 0:
                if stone in cache:
                    left, right = cache[stone]
                else:
                    half = length // 2
                    power = 10 ** half
                    right = stone % power
                    left = stone // power
                    cache[stone] = left, right
                new_counts[left] += count
                new_counts[right] += count
            else:
                new_counts[stone * 2024] += count
    return new_counts


def part_a(data):
    counts = parse_data(data)
    cache = dict()

    for _ in range(25):
        counts = blink(counts, cache)
    return sum(counts.values())


def part_b(data):
    counts = parse_data(data)
    cache = dict()

    for _ in range(75):
        counts = blink(counts, cache)
    return sum(counts.values())


def main():
    examples = [
        ("125 17", 55312, None)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
