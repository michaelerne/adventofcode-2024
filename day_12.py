from collections import deque

from run_util import run_puzzle

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def parse_data(data):
    grid = [list(row) for row in data.strip().split("\n")]
    rows, cols = len(grid), len(grid[0])
    return grid, rows, cols


def in_bounds(x, y, rows, cols):
    return 0 <= x < rows and 0 <= y < cols


def bfs(grid, start_x, start_y, seen, rows, cols):
    queue = deque([(start_x, start_y)])
    plant_type = grid[start_x][start_y]
    area = 0
    perimeter = {direction: set() for direction in DIRECTIONS}
    seen.add((start_x, start_y))

    while queue:
        x, y = queue.popleft()
        area += 1

        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy

            if in_bounds(nx, ny, rows, cols) and grid[nx][ny] == plant_type:
                if (nx, ny) not in seen:
                    seen.add((nx, ny))
                    queue.append((nx, ny))
            else:
                perimeter[(dx, dy)].add((x, y))

    return area, perimeter


def sides(perimeter):
    count = 0
    for direction, boundary_points in perimeter.items():
        seen = set()
        for point in boundary_points:
            if point not in seen:
                count += 1
                queue = deque([point])
                while queue:
                    current_point = queue.popleft()
                    if current_point in seen:
                        continue
                    seen.add(current_point)
                    x, y = current_point
                    for dx, dy in DIRECTIONS:
                        neighbor = (x + dx, y + dy)
                        if neighbor in boundary_points and neighbor not in seen:
                            queue.append(neighbor)
    return count


def cost(data, fn):
    grid, rows, cols = parse_data(data)

    seen = set()
    total_price = 0

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in seen:
                area, perimeter = bfs(grid, row, col, seen, rows, cols)
                total_price += fn(area, perimeter)

    return total_price


def part_a(data):
    return cost(data, lambda area, perimeter: area * sum(len(points) for points in perimeter.values()))


def part_b(data):
    return cost(data, lambda area, perimeter: area * sides(perimeter))


def main():
    examples = [
        ("""AAAA
BBCD
BBCC
EEEC""", 140, 80),
        ("""OOOOO
OXOXO
OOOOO
OXOXO
OOOOO""", 772, 436),
        ("""RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE""", 1930, 1206),
        ("""EEEEE
EXXXX
EEEEE
EXXXX
EEEEE""", 692, 236),
        ("""AAA
ABA
AAA""", 132, 68)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
