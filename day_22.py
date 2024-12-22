MASK_24 = (1 << 24) - 1
NUM_SEQUENCES = 20 ** 4


def parse_data(data: str) -> list[int]:
    lines = data.strip().splitlines()
    return [int(line) for line in lines if line.strip()]


def part_a(data: str) -> int:
    buyers = parse_data(data)

    total = 0
    for secret in buyers:
        for _ in range(2000):
            secret = (secret ^ (secret << 6)) & MASK_24
            secret ^= (secret >> 5)
            secret = (secret ^ (secret << 11)) & MASK_24
        total += secret

    return total


def part_b(data: str) -> int:
    buyers = parse_data(data)

    sequence_sale_sums = [0] * NUM_SEQUENCES
    last_buyer_for_sequence = [0] * NUM_SEQUENCES

    buyer_id = 0
    for secret in buyers:
        buyer_id += 1

        p_current = secret % 10

        window = 0
        for i in range(3):
            secret = (secret ^ (secret << 6)) & MASK_24
            secret ^= (secret >> 5)
            secret = (secret ^ (secret << 11)) & MASK_24

            p_new = secret % 10
            diff = (p_new - p_current) % 20

            window = (window * 20 + diff) % NUM_SEQUENCES
            p_current = p_new

        for i in range(1997):
            if last_buyer_for_sequence[window] != buyer_id:
                sequence_sale_sums[window] += p_current
                last_buyer_for_sequence[window] = buyer_id

            secret = (secret ^ (secret << 6)) & MASK_24
            secret ^= (secret >> 5)
            secret = (secret ^ (secret << 11)) & MASK_24

            p_new = secret % 10
            diff = (p_new - p_current) % 20
            window = (window * 20 + diff) % NUM_SEQUENCES

            p_current = p_new

        if last_buyer_for_sequence[window] != buyer_id:
            sequence_sale_sums[window] += p_current
            last_buyer_for_sequence[window] = buyer_id

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
    from run_util import run_puzzle
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
