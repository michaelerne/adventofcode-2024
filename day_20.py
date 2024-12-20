from collections import deque
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
    dist = [[None] * cols for _ in range(rows)]
    q = deque(start_positions)
    for (sx, sy) in start_positions:
        dist[sx][sy] = 0
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    while q:
        x, y = q.popleft()
        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if grid[nx][ny] != '#' and dist[nx][ny] is None:
                    dist[nx][ny] = dist[x][y] + 1
                    q.append((nx, ny))
    return dist

def get_cheats(grid, start, end, cheat_length, threshold=100):
    dist_from_start = bfs_distances(grid, [start])
    dist_to_end = bfs_distances(grid, [end])

    distance_no_cheat = dist_from_start[end[0]][end[1]]
    rows = len(grid)
    cols = len(grid[0])

    above_threshold = 0

    for xA in range(rows):
        for yA in range(cols):
            if dist_from_start[xA][yA] is not None and grid[xA][yA] != '#':
                xmin = max(0, xA - cheat_length)
                xmax = min(rows - 1, xA + cheat_length)
                ymin = max(0, yA - cheat_length)
                ymax = min(cols - 1, yA + cheat_length)

                for xB in range(xmin, xmax + 1):
                    dx = abs(xB - xA)
                    max_dy = cheat_length - dx
                    nymin = max(ymin, yA - max_dy)
                    nymax = min(ymax, yA + max_dy)
                    for yB in range(nymin, nymax + 1):
                        if grid[xB][yB] != '#':
                            dy = abs(yB - yA)
                            man_dist = dx + dy
                            if man_dist <= cheat_length:
                                time_with_cheat = dist_from_start[xA][yA] + man_dist + dist_to_end[xB][yB]
                                saving = distance_no_cheat - time_with_cheat
                                if saving >= threshold:
                                    above_threshold += 1

    return above_threshold

def part_a(data):
    grid, start, end = parse_data(data)
    return get_cheats(grid, start, end, cheat_length=2, threshold=100)

def part_b(data):
    grid, start, end = parse_data(data)
    return get_cheats(grid, start, end, cheat_length=20, threshold=100)

def main():
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, [])

if __name__ == '__main__':
    main()
