from run_util import run_puzzle


def parse_data(data):
    grid = {
        (x, y): char
        for y, row in enumerate(data.split('\n'))
        for x, char in enumerate(row)
    }
    max_x, max_y = max(grid.keys())
    return grid, max_x, max_y


def part_a(data):
    grid, max_x, max_y = parse_data(data)

    return sum(
        all(
            'XMAS'[n] == grid.get((x + d_x * n, y + d_y * n), "")
            for n in range(1, 4)
        )
        for y in range(max_y + 1)
        for x in range(max_x + 1)
        for d_x, d_y in (
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        )
        if grid[(x, y)] == 'X'
    )


def part_b(data):
    grid, max_x, max_y = parse_data(data)

    return sum(
        all(
            grid.get((x - 1, y - d_y), "") + grid.get((x + 1, y + d_y), "")
            in ("MS", "SM")
            for d_y in (-1, 1)
        )
        for y in range(max_y + 1)
        for x in range(max_x + 1)
        if grid[(x, y)] == 'A'
    )


def main():
    examples = [
        ("""MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""", 18, None),
        (""".M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........""", None, 9)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
