from collections import deque
from typing import List, Union

from run_util import run_puzzle


def parse_data(data):
    lines = data.strip('\n').split('\n')
    grid = [list(line) for line in lines]
    start = None
    end = None
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == 'S':
                start = (y, x)
            elif char == 'E':
                end = (y, x)
    return grid, start, end


def bfs_distances(grid, start_positions):
    rows = len(grid)
    cols = len(grid[0])
    dist: List[List[Union[None, int]]] = [[None] * cols for _ in range(rows)]
    queue = deque(start_positions)
    for (sx, sy) in start_positions:
        dist[sx][sy] = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        x, y = queue.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if grid[nx][ny] != '#' and dist[nx][ny] is None:
                    dist[nx][ny] = dist[x][y] + 1
                    queue.append((nx, ny))
    return dist


def get_cheats(grid, start, end, cheat_length):
    dist_from_start = bfs_distances(grid, [start])
    dist_to_end = bfs_distances(grid, [end])

    distance_no_cheat = dist_from_start[end[0]][end[1]]

    rows = len(grid)
    cols = len(grid[0])
    is_track = [[(grid[x][y] != '#') for y in range(cols)] for x in range(rows)]

    a_candidates = [
        (x, y)
        for x in range(rows)
        for y in range(cols)
        if dist_from_start[x][y] is not None and is_track[x][y]
    ]

    best_savings = {}

    for (xa, y_a) in a_candidates:
        xmin = max(0, xa - cheat_length)
        xmax = min(rows - 1, xa + cheat_length)
        ymin = max(0, y_a - cheat_length)
        ymax = min(cols - 1, y_a + cheat_length)
        for xB in range(xmin, xmax + 1):
            dx = abs(xB - xa)
            max_dy = cheat_length - dx
            nymin = max(ymin, y_a - max_dy)
            nymax = min(ymax, y_a + max_dy)
            for yB in range(nymin, nymax + 1):
                if is_track[xB][yB]:
                    dy = abs(yB - y_a)
                    man_dist = dx + dy
                    if man_dist <= cheat_length:
                        time_with_cheat = dist_from_start[xa][y_a] + man_dist + dist_to_end[xB][yB]
                        saving = distance_no_cheat - time_with_cheat
                        if saving >= 0:
                            cheat_id = (xa, y_a, xB, yB)
                            if cheat_id not in best_savings or best_savings[cheat_id] < saving:
                                best_savings[cheat_id] = saving

    savings_distribution = {}
    for s in best_savings.values():
        savings_distribution[s] = savings_distribution.get(s, 0) + 1

    return savings_distribution


def part_a(data):
    grid, start, end = parse_data(data)
    cheats_distribution = get_cheats(grid, start, end, cheat_length=2)
    count = sum(c for s, c in cheats_distribution.items() if s >= 100)
    return count


def part_b(data):
    grid, start, end = parse_data(data)
    cheats_distribution = get_cheats(grid, start, end, cheat_length=20)
    count = sum(c for s, c in cheats_distribution.items() if s >= 100)
    return count


def main():
    example_data = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""
    grid, start, end = parse_data(example_data)
    cheats = get_cheats(grid, start, end, 2)
    for number_of_cheats, picoseconds in [(14, 2), (14, 4), (2, 6), (4, 8), (2, 10), (3, 12), (1, 20), (1, 38), (1, 40), (1, 64)]:
        assert cheats[picoseconds] == number_of_cheats
    cheats = get_cheats(grid, start, end, 20)
    for number_of_cheats, picoseconds in [(32, 50), (31, 52), (29, 54), (39, 56), (25, 58), (23, 60), (20, 62), (19, 64), (12, 66), (14, 68), (12, 70), (22, 72), (4, 74), (3, 76)]:
        assert cheats[picoseconds] == number_of_cheats

    examples = [(example_data, 0, 0)]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
