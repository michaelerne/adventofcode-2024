from run_util import run_puzzle


def parse_schematic(block):
    order, schematic_type = (range(1, 6), 'lock') if block[0].count('#') == 5 and block[-1].count('.') == 5 else (range(5, 0, -1), 'key')
    heights = [
        sum(
            1
            for row in order
            if block[row][col] == '#'
        )
        for col in range(5)
    ]
    return heights, schematic_type


def parse_data(data):
    locks = []
    keys = []

    for block in data.strip().split('\n\n'):
        heights, schematic_type = parse_schematic(block.split('\n'))
        if schematic_type == 'lock':
            locks.append(heights)
        elif schematic_type == 'key':
            keys.append(heights)

    return locks, keys


def part_a(data):
    locks, keys = parse_data(data)

    return sum(
        1
        for lock in locks
        for key in keys
        if all(lock[i] + key[i] <= 5 for i in range(5))

    )


def main():
    examples = [
        (
            # Example from the puzzle prompt
            """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
""",
            3,
            None
        )
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, None, examples)


if __name__ == '__main__':
    main()
