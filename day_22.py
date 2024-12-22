from collections import defaultdict

from run_util import run_puzzle

MASK_24 = 0xFFFFFF


def parse_data(data):
    lines = data.strip().splitlines()
    return [int(line) for line in lines if line.strip()]


def part_a(data):
    data = parse_data(data)

    total = 0
    for secret in data:
        x = secret
        for _ in range(2000):
            x ^= (x << 6) & MASK_24
            x ^= (x >> 5)
            x ^= (x << 11) & MASK_24

        total += x
    return total


def part_b(data):
    data = parse_data(data)

    global_sequence_sums = defaultdict(int)

    for secret in data:
        x = secret

        seen_for_buyer = {}

        price_current = x % 10
        diff0 = diff1 = diff2 = None

        for i in range(2000):
            x ^= (x << 6) & MASK_24
            x ^= (x >> 5)
            x ^= (x << 11) & MASK_24

            price_new = x % 10

            diff3 = price_new - price_current
            if i >= 3:
                seq = (diff0, diff1, diff2, diff3)
                if seq not in seen_for_buyer:
                    seen_for_buyer[seq] = price_new

            diff0, diff1, diff2 = diff1, diff2, diff3
            price_current = price_new

        for seq, sale_price in seen_for_buyer.items():
            global_sequence_sums[seq] += sale_price

    return max(global_sequence_sums.values())


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
