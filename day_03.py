from run_util import run_puzzle
import re


def part_a(data):
    matches = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', data)
    return sum(int(a) * int(b) for a, b in matches)


def part_b(data):
    matches = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don\'t\(\))', data)
    solution = 0
    enabled = True
    for a, b, do, do_not in matches:
        if do or do_not:  # there is no try
            enabled = bool(do)
        elif enabled:
            solution += int(a) * int(b)
    return solution


def main():
    examples = [
        ("""xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
""", 161, None),
        ("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))", None, 48)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
