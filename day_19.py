from collections import deque

from run_util import run_puzzle


class AhoCorasick:
    def __init__(self, patterns=None):
        self.edges = []
        self.fail = []
        self.out = []
        self._make_node()

        if patterns:
            for pattern in patterns:
                self.add_pattern(pattern)
            self.build()

    def _make_node(self):
        self.edges.append({})
        self.fail.append(0)
        self.out.append([])
        return len(self.edges) - 1

    def add_pattern(self, pattern):
        node = 0
        for ch in pattern:
            if ch not in self.edges[node]:
                self.edges[node][ch] = self._make_node()
            node = self.edges[node][ch]
        self.out[node].append(len(pattern))

    def build(self):
        queue = deque()
        for char, next_idx in self.edges[0].items():
            self.fail[next_idx] = 0
            queue.append(next_idx)

        while queue:
            r = queue.popleft()
            for char, next_idx in self.edges[r].items():
                queue.append(next_idx)
                f = self.fail[r]
                while f > 0 and char not in self.edges[f]:
                    f = self.fail[f]
                self.fail[next_idx] = self.edges[f][char] if char in self.edges[f] else 0
                self.out[next_idx].extend(self.out[self.fail[next_idx]])

    def find_all(self, text):
        node = 0
        matches_at = [[] for _ in range(len(text))]
        for i, char in enumerate(text):
            while node > 0 and char not in self.edges[node]:
                node = self.fail[node]
            node = self.edges[node][char] if char in self.edges[node] else 0
            for pat_len in self.out[node]:
                matches_at[i].append(pat_len)
        return matches_at


def parse_data(data):
    lines = [line.strip() for line in data.split('\n') if line.strip()]
    patterns_line = lines[0]
    patterns = [p.strip() for p in patterns_line.split(',')]
    designs = lines[1:]

    ac = AhoCorasick(patterns)

    return ac, designs

def get_options(ac, designs):
    total_ways = []
    for design in designs:
        matches_at = ac.find_all(design)
        n = len(design)
        ways = [0] * (n + 1)
        ways[0] = 1

        for i in range(n):
            for pat_len in matches_at[i]:
                old_pos = i + 1 - pat_len
                if old_pos >= 0 and ways[old_pos]:
                    ways[i + 1] += ways[old_pos]

        total_ways.append(ways[n])

    return total_ways


def part_a(data):
    ac, designs = parse_data(data)

    return sum(1 for option in get_options(ac, designs) if option)


def part_b(data):
    ac, designs = parse_data(data)

    return sum(get_options(ac, designs))


def main():
    examples = [("""r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb""", 6, 16)]

    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
