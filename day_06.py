from run_util import run_puzzle

D_X = (0, 1, 0, -1)
D_Y = (-1, 0, 1, 0)


def parse_data(data):
    grid = {
        (x, y): cell
        for y, row in enumerate(data.strip().split('\n'))
        for x, cell in enumerate(row)
    }
    max_x, max_y = max((x + 1, y + 1) for x, y in grid.keys())
    start = min(position for position, cell in grid.items() if cell == '^')
    return grid, max_x, max_y, start


def patrol(grid, start):
    position, direction, patrol_path = start, 0, set()
    while position in grid:
        patrol_path.add(position)
        next_position = (
            position[0] + D_X[direction],
            position[1] + D_Y[direction]
        )
        if grid.get(next_position) == '#':
            direction = (direction + 1) % 4
        else:
            position = next_position
    return patrol_path

def part_a(data):
    grid, max_x, max_y, start = parse_data(data)

    return len(patrol(grid, start))


def part_b(data):
    grid, max_x, max_y, start = parse_data(data)

    # get relevant places for obstacles
    patrol_path = patrol(grid, start)

    # calculate jump lookup table
    jump_lookup = {}
    for x in range(max_x):
        # >
        line = ((x, -1), 1)
        for y in range(max_y):
            if grid.get((x, y)) == '#':
                line = ((x, y + 1), 1)
            jump_lookup[(x, y, 0)] = line
        # <
        line = ((x, max_y), 3)
        for y in range(max_y - 1, -1, -1):
            if grid.get((x, y)) == '#':
                line = ((x, y - 1), 3)
            jump_lookup[(x, y, 2)] = line
    for y in range(max_y):
        # ^
        line = ((-1, y), 0)
        for x in range(max_x):
            if grid.get((x, y)) == '#':
                line = ((x + 1, y), 0)
            jump_lookup[(x, y, 3)] = line
        # v
        line = ((max_x, y), 2)
        for x in range(max_x - 1, -1, -1):
            if grid.get((x, y)) == '#':
                line = ((x - 1, y), 2)
            jump_lookup[(x, y, 1)] = line

    # attempt relevant positions
    options = 0
    for step in patrol_path:
        if grid[step] != '.':
            continue
        position, direction, path = start, 0, set()
        while position in grid and (position, direction) not in path:
            path.add((position, direction))
            if position[0] != step[0] and position[1] != step[1]:
                position, direction = jump_lookup[(*position, direction)]
            else:
                next_position = (
                    position[0] + D_X[direction],
                    position[1] + D_Y[direction]
                )
                if grid.get(next_position) == '#' or next_position == step:
                    direction = (direction + 1) % 4
                else:
                    position = next_position
        if (position, direction) in path:
            options += 1
    return options


def main():
    examples = [
        ("""....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...""", 41, 6)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
