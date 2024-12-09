from collections import defaultdict
from itertools import combinations
from math import gcd

from run_util import run_puzzle


def parse_data(data):
    rows = data.strip().split('\n')

    antenna_positions = defaultdict(list)
    antenna_pairs = {}
    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            if char != '.':
                antenna_positions[char].append((x, y))

    for frequency, positions in antenna_positions.items():
        antenna_pairs[frequency] = list(combinations(positions, 2))

    height, width = len(rows), len(rows[0])
    valid_x = set(range(width))
    valid_y = set(range(height))

    return antenna_positions, antenna_pairs, valid_x, valid_y


def part_a(data):
    _, antenna_pairs, valid_x, valid_y = parse_data(data)

    antinodes = set()

    for frequency, pairs in antenna_pairs.items():
        for (x1, y1), (x2, y2) in pairs:
            dx, dy = x2 - x1, y2 - y1
            potential_antinodes = [
                (x1 - dx, y1 - dy),
                (x2 + dx, y2 + dy)
            ]

            antinodes.update((ax, ay) for ax, ay in potential_antinodes if ax in valid_x and ay in valid_y)

    return len(antinodes)


def part_b(data):
    antenna_positions, antenna_pairs, valid_x, valid_y = parse_data(data)

    antinodes = set()

    for frequency, pairs in antenna_pairs.items():
        if len(antenna_positions[frequency]) > 1:
            antinodes.update(antenna_positions[frequency])

        for (x1, y1), (x2, y2) in pairs:
            dx, dy = x2 - x1, y2 - y1
            for direction in (-1, 1):
                px, py = x1, y1
                while (px + direction * dx) in valid_x and (py + direction * dy) in valid_y:
                    px, py = px + direction * dx, py + direction * dy
                    antinodes.add((px, py))

    return len(antinodes)


def main():
    examples = [
        ("""............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............""", 14, 34)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
