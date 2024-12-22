from run_util import run_puzzle

MASK_24 = (1 << 24) - 1
BASE = 19
OFFSET = 9
SIZE = BASE ** 4


def parse_data(data):
    lines = data.strip().splitlines()
    return [int(line) for line in lines if line.strip()]


def part_a(data):
    data = parse_data(data)

    total = 0
    for secret in data:
        for _ in range(2000):
            secret = (secret ^ (secret << 6)) & MASK_24
            secret = secret ^ (secret >> 5)
            secret = (secret ^ (secret << 11)) & MASK_24
        total += secret

    return total


def part_b(data):
    buyers = parse_data(data)

    sequence_sale_sums = [0] * SIZE
    last_buyer_for_sequence = [0] * SIZE

    for buyer_id, secret in enumerate(buyers, start=1):

        price_current = secret % 10

        diff0 = diff1 = diff2 = None

        for i in range(2000):
            secret = (secret ^ (secret << 6)) & MASK_24
            secret = secret ^ (secret >> 5)
            secret = (secret ^ (secret << 11)) & MASK_24

            price_new = secret % 10
            diff3 = price_new - price_current

            if i >= 3:
                index = (diff0 + OFFSET)
                index = index * 19 + (diff1 + OFFSET)
                index = index * 19 + (diff2 + OFFSET)
                index = index * 19 + (diff3 + OFFSET)

                if last_buyer_for_sequence[index] != buyer_id:
                    sequence_sale_sums[index] += price_new
                    last_buyer_for_sequence[index] = buyer_id

            diff0, diff1, diff2 = diff1, diff2, diff3
            price_current = price_new

    return max(sequence_sale_sums)


def main():
    examples = [
        (
            """1
10
100
2024
""",
            37327623,
            None
        ),
        (
            """1
2
3
2024
""",
            None,
            23
        )
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
