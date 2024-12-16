import heapq
from collections import deque

from run_util import run_puzzle

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
STEP_COST = 1
TURN_COST = 1000


def parse_data(data):
    grid = [list(line) for line in data.strip('\n').split('\n')]
    start = None
    end = None
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == 'S':
                start = (y, x)
            elif char == 'E':
                end = (y, x)
    return grid, start, end


def run_dijkstra(grid, start):
    costs = [[[float('inf')] * 4 for _ in range(len(grid[0]))] for __ in range(len(grid))]

    queue = []
    heapq.heappush(queue, (0, *start, 1))

    while queue:
        cost, x, y, direction = heapq.heappop(queue)
        if cost > costs[x][y][direction]:
            continue

        d_x, d_y = DIRECTIONS[direction]
        next_x, next_y = x + d_x, y + d_y
        if grid[next_x][next_y] != '#':
            new_cost = cost + STEP_COST
            if new_cost < costs[next_x][next_y][direction]:
                costs[next_x][next_y][direction] = new_cost
                heapq.heappush(queue, (new_cost, next_x, next_y, direction))

        left_direction = (direction - 1) % 4
        new_cost = cost + TURN_COST
        if new_cost < costs[x][y][left_direction]:
            costs[x][y][left_direction] = new_cost
            heapq.heappush(queue, (new_cost, x, y, left_direction))

        right_direction = (direction + 1) % 4
        new_cost = cost + TURN_COST
        if new_cost < costs[x][y][right_direction]:
            costs[x][y][right_direction] = new_cost
            heapq.heappush(queue, (new_cost, x, y, right_direction))

    return costs


def get_min_cost(dist, end):
    end_x, end_y = end
    return min(dist[end_x][end_y])


def find_tiles_on_best_paths(grid, costs, end):
    height, width = len(grid), len(grid[0])
    min_cost = get_min_cost(costs, end)

    on_path = [[[False] * 4 for _ in range(width)] for __ in range(height)]
    queue = deque()

    end_x, end_y = end
    for direction in range(4):
        if costs[end_x][end_y][direction] == min_cost:
            on_path[end_x][end_y][direction] = True
            queue.append((end_x, end_y, direction))

    while queue:
        x, y, direction = queue.popleft()
        cost_here = costs[x][y][direction]

        d_x, d_y = DIRECTIONS[direction]
        previous_x, previous_y = x - d_x, y - d_y
        if grid[previous_x][previous_y] != '#':
            if costs[previous_x][previous_y][direction] + STEP_COST == cost_here:
                if not on_path[previous_x][previous_y][direction]:
                    on_path[previous_x][previous_y][direction] = True
                    queue.append((previous_x, previous_y, direction))

        direction_left = (direction + 1) % 4
        if costs[x][y][direction_left] + TURN_COST == cost_here:
            if not on_path[x][y][direction_left]:
                on_path[x][y][direction_left] = True
                queue.append((x, y, direction_left))

        direction_right = (direction - 1) % 4
        if costs[x][y][direction_right] + TURN_COST == cost_here:
            if not on_path[x][y][direction_right]:
                on_path[x][y][direction_right] = True
                queue.append((x, y, direction_right))

    return sum(
        1 for i in range(height) for j in range(width)
        if grid[i][j] != '#' and any(on_path[i][j][direction] for direction in range(4))
    )


def part_a(data):
    grid, start, end = parse_data(data)
    costs = run_dijkstra(grid, start)
    return get_min_cost(costs, end)


def part_b(data):
    grid, start, end = parse_data(data)
    costs = run_dijkstra(grid,start)
    return find_tiles_on_best_paths(grid, costs, end)


def main():
    example_map_1 = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

    example_map_2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.# 
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.# 
#S#.............#
#################"""

    examples = [
        (example_map_1, 7036, 45),
        (example_map_2, 11048, 64)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
