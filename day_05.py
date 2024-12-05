from functools import cmp_to_key

from run_util import run_puzzle


def parse_data(data):
    rules_data, updates_data = data.strip().split('\n\n')

    rules = [tuple(map(int, line.split('|'))) for line in rules_data.split('\n')]
    updates = [[int(page) for page in line.split(',') if page] for line in updates_data.split('\n')]
    pairs = [{page: position for (position, page) in enumerate(update)} for update in updates]

    return rules, updates, pairs


def part_a(data):
    rules, updates, pairs = parse_data(data)
    return sum(
        update[len(update) // 2]
        for update, pairs in zip(updates, pairs)
        if all((x not in pairs) or (y not in pairs) or pairs[x] < pairs[y] for (x, y) in rules)
    )


def part_b(data):
    rules, updates, pairs = parse_data(data)

    return sum(
        sorted(update, key=cmp_to_key(lambda x, y: 2 * ((x, y) in rules) - 1), reverse=True)[len(update) // 2]
        for update, pairs in zip(updates, pairs)
        if not all((x not in pairs) or (y not in pairs) or pairs[x] < pairs[y] for (x, y) in rules)
    )


def main():
    examples = [
        ("""47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
""", 143, 123)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
