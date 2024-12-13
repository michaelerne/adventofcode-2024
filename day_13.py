import re
from typing import Tuple

from run_util import run_puzzle

PART_B_OFFSET = 10_000_000_000_000


def parse_data(data: str, part_b: bool = False) -> list[Tuple[int, int, int, int, int, int]]:

    pattern = re.compile(
        r'Button A:\s*X\+(\d+),\s*Y\+(\d+)\s*'
        r'Button B:\s*X\+(\d+),\s*Y\+(\d+)\s*'
        r'Prize:\s*X=(\d+),\s*Y=(\d+)',
        re.MULTILINE
    )

    machines = []
    for match in pattern.finditer(data):
        a_x, a_y, b_x, b_y, prize_x, prize_y = map(int, match.groups())
        machines.append((a_x, a_y, b_x, b_y, prize_x + PART_B_OFFSET if part_b else prize_x, prize_y + PART_B_OFFSET if part_b else prize_y))

    return machines


def cost(a_x:int, a_y:int, b_x:int, b_y:int, x_prize:int, y_prize:int) -> int:
    a = (b_x * y_prize - b_y * x_prize) // (a_y * b_x - a_x * b_y)
    b = (x_prize - a * a_x) // b_x
    if (x_prize - a * a_x) % b_x == 0 and (b_x * y_prize - b_y * x_prize) % (a_y * b_x - a_x * b_y) == 0:
        return 3 * a + b
    return 0


def part_a(data:str) -> int:
    machines = parse_data(data)
    return sum(cost(*machine) for machine in machines)


def part_b(data:str) -> int:
    machines = parse_data(data, part_b=True)
    return sum(cost(*machine) for machine in machines)


def main():
    examples = [
        ("""Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279""", 480, 875318608908)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
