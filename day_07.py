from run_util import run_puzzle


def parse_data(data):
    lines = []
    for line in data.strip().split('\n'):
        left, right = line.split(': ')
        result = int(left)
        numbers = list(map(int, right.split()))
        lines.append((result, numbers))
    return lines


def is_valid(numbers, expected_result, part_b=False):
    memo = {}

    def backtrack(index, current_result):
        if index == len(numbers):
            return current_result == expected_result

        key = (index, current_result)
        if key in memo:
            return memo[key]

        next_num = numbers[index]

        if current_result > expected_result:
            memo[key] = False
            return False

        operations = ['+', '*']
        if part_b:
            operations.append('|')

        for op in operations:
            if op == '+':
                if backtrack(index + 1, current_result + next_num):
                    return True
            elif op == '*':
                if backtrack(index + 1, current_result * next_num):
                    return True
            elif op == '|' and part_b:
                # Arithmetic concatenation for '|'
                concatenated = current_result * (10 ** len(str(next_num))) + next_num
                if backtrack(index + 1, concatenated):
                    return True

        memo[key] = False
        return False

    return backtrack(1, numbers[0])


def part_a(data):
    data = parse_data(data)

    return sum(
        result
        for result, numbers in data
        if is_valid(numbers, result)
    )


def part_b(data):
    data = parse_data(data)

    return sum(
        result
        for result, numbers in data
        if is_valid(numbers, result, part_b=True)
    )


def main():
    examples = [
        ("""190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20""", 3749, 11387)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
