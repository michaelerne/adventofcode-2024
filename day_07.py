from run_util import run_puzzle


def parse_data(data):
    return (
        (tuple(int(num) for num in right.split()), int(left))
        for left, right in (line.split(': ') for line in data.strip().split('\n'))
    )


def is_valid(numbers, expected_result, part_b=False):
    def backtrack(index, current_result):
        if index < 0:
            return current_result == 0

        last_number = numbers[index]

        if part_b:
            remaining_last_number = last_number
            remaining_result = current_result
            valid = True
            while remaining_last_number > 0:
                if remaining_last_number % 10 == remaining_result % 10:
                    remaining_result //= 10
                    remaining_last_number //= 10
                else:
                    valid = False
                    break
            if valid:
                if backtrack(index - 1, remaining_result):
                    return True

        if backtrack(index - 1, current_result - last_number):
            return True

        if current_result % last_number == 0 and backtrack(index - 1, current_result // last_number):
            return True

        return False

    return backtrack(len(numbers) - 1, expected_result)


def part_a(data):
    data = parse_data(data)

    return sum(
        result
        for numbers, result  in data
        if is_valid(numbers, result)
    )


def part_b(data):
    data = parse_data(data)

    return sum(
        result
        for numbers, result  in data
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
