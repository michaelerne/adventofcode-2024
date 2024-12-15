from collections import deque

from run_util import run_puzzle

DIRECTIONS = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1)
}


def parse_data(data):
    parts = data.strip('\n').split('\n\n')
    map_part = parts[0].split('\n')
    moves = [char for row in parts[1].split('\n') for char in row]

    grid = []
    for y, line in enumerate(map_part):
        if '@' in line:
            robot_x = line.index('@')
            robot_y = y
            line.replace('@', '.')
        grid.append(list(line.replace('@', '.')))

    return grid, moves, (robot_y, robot_x)


def scale_map(grid, robot_y, robot_x):
    # '#' -> '##'
    # 'O' -> '[]'
    # '.' -> '..'
    new_grid = []

    for y, row in enumerate(grid):
        new_row = []
        for x, ch in enumerate(row):
            if ch == '#':
                new_row += ["#", "#"]
            elif ch == 'O':
                new_row += ['[', ']']
            elif ch == '.':
                new_row += ['.', '.']
        new_grid.append(new_row)

    robot_x *= 2

    return new_grid, (robot_y, robot_x)


def is_box_char(ch, part_b):
    if part_b:
        return ch in ['[', ']']
    else:
        return ch == 'O'


def is_wall(ch):
    return ch == '#'


def is_empty(ch):
    return ch == '.'


def get_box_positions(y, x, grid, part_b):
    if part_b:
        if grid[y][x] == '[':
            return [(y, x), (y, x + 1)]
        else:
            return [(y, x - 1), (y, x)]
    else:
        return [(y, x)]


def find_box_start(y, x, grid, part_b):
    if not part_b:
        return y, x
    else:
        if grid[y][x] == '[':
            return y, x
        else:
            return y, x - 1


def can_push_and_collect_boxes(grid, robot_y, robot_x, dy, dx, part_b):
    queue = deque([(robot_y, robot_x)])
    seen = set()
    boxes_to_move = set()

    while queue:
        y, x = queue.popleft()
        if (y, x) in seen:
            continue
        seen.add((y, x))

        fy, fx = y + dy, x + dx
        char = grid[fy][fx]
        if is_wall(char):
            return False, []

        if is_empty(char):
            continue

        if is_box_char(char, part_b):
            box_start = find_box_start(fy, fx, grid, part_b)
            for (by, bx) in get_box_positions(box_start[0], box_start[1], grid, part_b):
                queue.append((by, bx))
            boxes_to_move.add(box_start)

    return True, list(boxes_to_move)


def do_push(grid, boxes_to_move, dy, dx, part_b):
    old_positions = []
    for (by, bx) in boxes_to_move:
        box_positions = get_box_positions(by, bx, grid, part_b)
        for (oy, ox) in box_positions:
            grid[oy][ox] = '.'
        old_positions.append((by, bx))

    for (by, bx) in old_positions:
        if part_b:
            grid[by + dy][bx + dx] = '['
            grid[by + dy][bx + dx + 1] = ']'
        else:
            grid[by + dy][bx + dx] = 'O'


def simulate_moves(grid, moves, robot_y, robot_x, part_b=False):
    for move in moves:
        dy, dx = DIRECTIONS[move]
        ny, nx = robot_y + dy, robot_x + dx
        next_char = grid[ny][nx]

        if is_wall(next_char):
            continue

        if is_empty(next_char):
            robot_y, robot_x = ny, nx
            continue

        if is_box_char(next_char, part_b):
            can_push, boxes = can_push_and_collect_boxes(grid, robot_y, robot_x, dy, dx, part_b)
            if not can_push:
                continue
            do_push(grid, boxes, dy, dx, part_b)
            robot_y, robot_x = ny, nx

    return grid


def compute_final_sum(grid, box_char):
    return sum(
        100 * y + x
        for y in range(len(grid))
        for x in range(len(grid[0]))
        if grid[y][x] == box_char
    )


def part_a(data):
    grid, moves, (robot_y, robot_x) = parse_data(data)

    grid = simulate_moves(grid, moves, robot_y, robot_x, part_b=False)
    return compute_final_sum(grid, box_char='O')


def part_b(data):
    grid, moves, (robot_y, robot_x) = parse_data(data)
    grid, (robot_y, robot_x) = scale_map(grid, robot_y, robot_x)

    grid = simulate_moves(grid, moves, robot_y, robot_x, part_b=True)
    return compute_final_sum(grid, box_char='[')


def main():
    example_1 = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

    example_2 = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""

    example_3 = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

    examples = [
        (example_1, 2028, None),
        (example_2, None, 618),
        (example_3, 10092, 9021)
    ]

    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
