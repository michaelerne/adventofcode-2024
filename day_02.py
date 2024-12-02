from run_util import run_puzzle


def parse_data(data):
    return [[int(x) for x in line.split()] for line in data.strip().split('\n')]


def all_decreasing(report):
    return report == sorted(report)


def all_increasing(report):
    return report[::-1] == sorted(report)


def has_safe_diffs(report):
    return all(1 <= abs(i - j) <= 3 for i, j in zip(report, report[1:]))


def is_safe(report):
    return has_safe_diffs(report) and (all_increasing(report) or all_decreasing(report))


def part_a(data):
    reports = parse_data(data)

    return sum(is_safe(report) for report in reports)


def part_b(data):
    reports = parse_data(data)

    return sum(
        any(
            is_safe(report[:i] + report[i + 1:]) for i in range(len(report))
        ) for report in reports
    )


def main():
    examples = [
        ("""7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9""", 2, 4)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
