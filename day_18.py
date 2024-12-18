from collections import deque

from run_util import run_puzzle


def parse_data(data):
    coordinates = []
    for line in data.strip().splitlines():
        x_str, y_str = line.split(',')
        coordinates.append((int(x_str), int(y_str)))
    max_x, max_y = max(x for x, _ in coordinates), max(y for _, y in coordinates)
    return coordinates, max_x + 1, (max_x, max_y)


def get_grid(coordinates, grid_size, steps):
    corrupted = [[False] * grid_size for _ in range(grid_size)]
    for i in range(steps):
        x, y = coordinates[i]
        corrupted[y][x] = True
    return corrupted


def get_path(corrupted, start, goal):
    grid_size = len(corrupted)

    visited = [[False] * grid_size for _ in range(grid_size)]
    visited[start[1]][start[0]] = True
    queue = deque([(start[0], start[1], 0)])
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while queue:
        x, y, dist = queue.popleft()
        if (x, y) == goal:
            return dist
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size:
                if not corrupted[ny][nx] and not visited[ny][nx]:
                    visited[ny][nx] = True
                    queue.append((nx, ny, dist + 1))


def part_a(data):
    coordinates, grid_size, goal = parse_data(data)
    steps_to_simulate = 12 if goal == (6, 6) else 1024
    corrupted = get_grid(coordinates, grid_size, steps_to_simulate)
    return get_path(corrupted, (0, 0), goal)


def part_b(data):
    coordinates, grid_size, goal = parse_data(data)
    low, high = 0, len(coordinates) - 1

    while low <= high:
        mid = (low + high) // 2

        if get_path(get_grid(coordinates, grid_size, mid + 1), (0, 0), goal):
            low = mid + 1
        else:
            high = mid - 1

    x, y = coordinates[low]
    return f"{x},{y}"


def main():
    examples = [
        ("""5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0""", 22, "6,1")
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
