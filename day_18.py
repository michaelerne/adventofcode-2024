from collections import deque

from run_util import run_puzzle

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def parse_data(data):
    coordinates = []
    for line in data.strip().splitlines():
        x_str, y_str = line.split(',')
        coordinates.append((int(x_str), int(y_str)))
    max_x = max(x for x, _ in coordinates)
    max_y = max(y for _, y in coordinates)
    grid_size = max(max_x, max_y) + 1
    return coordinates, grid_size, (max_x, max_y)


def precompute_corruption_times(coordinates, grid_size):
    max_steps = len(coordinates)
    corruption_times = [[max_steps + 1] * grid_size for _ in range(grid_size)]
    for i, (x, y) in enumerate(coordinates):
        if 0 <= x < grid_size and 0 <= y < grid_size:
            corruption_time = i + 1
            if corruption_time < corruption_times[y][x]:
                corruption_times[y][x] = corruption_time
    return corruption_times


def part_a(data):
    coordinates, grid_size, goal = parse_data(data)
    corruption_times = precompute_corruption_times(coordinates, grid_size)
    steps = 12 if goal == (6, 6) else 1024

    sx, sy = (0, 0)
    gx, gy = goal
    grid_size = len(corruption_times)

    visited_start = [[False] * grid_size for _ in range(grid_size)]
    dist_start = [[float('inf')] * grid_size for _ in range(grid_size)]
    visited_start[sy][sx] = True
    dist_start[sy][sx] = 0
    queue_start = deque([(sx, sy)])

    visited_goal = [[False] * grid_size for _ in range(grid_size)]
    dist_goal = [[float('inf')] * grid_size for _ in range(grid_size)]
    visited_goal[gy][gx] = True
    dist_goal[gy][gx] = 0
    queue_goal = deque([(gx, gy)])

    def expand(queue, visited_self, dist_self, visited_other, dist_other):
        for _ in range(len(queue)):
            x, y = queue.popleft()
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size:
                    if corruption_times[ny][nx] > steps and not visited_self[ny][nx]:
                        visited_self[ny][nx] = True
                        dist_self[ny][nx] = dist_self[y][x] + 1
                        if visited_other[ny][nx]:
                            return dist_self[ny][nx] + dist_other[ny][nx]
                        queue.append((nx, ny))

    while queue_start or queue_goal:
        meet_dist = expand(queue_start, visited_start, dist_start, visited_goal, dist_goal)
        if meet_dist is not None:
            return meet_dist
        meet_dist = expand(queue_goal, visited_goal, dist_goal, visited_start, dist_start)
        if meet_dist is not None:
            return meet_dist


def part_b(data):
    # https://www.reddit.com/r/adventofcode/comments/1hgy6nb/comment/m2nd7mu/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    coordinates, grid_size, goal = parse_data(data)
    corruption_times = precompute_corruption_times(coordinates, grid_size)
    max_steps = len(coordinates)

    queue = [deque() for _ in range(max_steps + 2)]
    visited = [[False] * grid_size for _ in range(grid_size)]

    gx, gy = goal
    queue[max_steps + 1].append((gx, gy))
    visited[gy][gx] = True

    for t in range(max_steps + 1, 0, -1):
        while queue[t]:
            x, y = queue[t].popleft()
            if (x, y) == (0, 0):
                bx, by = coordinates[t - 1]
                return f"{bx},{by}"
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size and not visited[ny][nx]:
                    corruption_time = corruption_times[ny][nx]
                    if corruption_time >= t:
                        visited[ny][nx] = True
                        queue[t].append((nx, ny))
                    else:
                        visited[ny][nx] = True
                        queue[corruption_time].append((nx, ny))


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
