from run_util import run_puzzle

D = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def parse_data(data):
    lines = data.strip().split("\n")
    grid = [[(ord(ch) - 48) if ('0' <= ch <= '9') else -1 for ch in line] for line in lines]
    rows = len(grid)
    cols = len(grid[0])
    heights = [[] for _ in range(10)]
    nines = []
    for x in range(rows):
        row = grid[x]
        for y in range(cols):
            h = row[y]
            if h == 9:
                nines.append((x, y))
            if h >= 0:
                heights[h].append((x, y))
    return grid, rows, cols, heights, nines


def total_score(grid, rows, cols, heights, nines):
    dp = [[0] * cols for _ in range(rows)]
    for i, (x, y) in enumerate(nines):
        dp[x][y] = 1 << i
    for h in range(8, -1, -1):
        hlist = heights[h]
        for i in range(len(hlist)):
            x, y = hlist[i]
            base = grid[x][y]
            val = 0
            for dx, dy in D:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == base + 1:
                    val |= dp[nx][ny]
            dp[x][y] = val
    total = 0
    for x, y in heights[0]:
        total += bin(dp[x][y]).count("1")
    return total


def total_rating(grid, rows, cols, heights):
    dp = [[0] * cols for _ in range(rows)]
    for x, y in heights[9]:
        dp[x][y] = 1
    for h in range(8, -1, -1):
        hlist = heights[h]
        for i in range(len(hlist)):
            x, y = hlist[i]
            base = grid[x][y]
            s = 0
            for dx, dy in D:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == base + 1:
                    s += dp[nx][ny]
            dp[x][y] = s
    total = 0
    for x, y in heights[0]:
        total += dp[x][y]
    return total


def part_a(data):
    grid, rows, cols, heights, nines = parse_data(data)
    return total_score(grid, rows, cols, heights, nines)


def part_b(data):
    grid, rows, cols, heights, nines = parse_data(data)
    return total_rating(grid, rows, cols, heights)


def main():
    examples = [
        ("""89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""", 36, 81)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
