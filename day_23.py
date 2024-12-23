from collections import defaultdict

from run_util import run_puzzle


def parse_data(data):
    adjacency = defaultdict(set)
    for line in data.strip().split('\n'):
        left, right = line.split('-')
        adjacency[left].add(right)
        adjacency[right].add(left)
    return adjacency


def part_a(data):
    adjacency = parse_data(data)
    found = set()
    for u in adjacency:
        if u.startswith('t'):
            neighbours = list(adjacency[u])
            for i in range(len(neighbours) - 1):
                for j in range(i + 1, len(neighbours)):
                    v, w = neighbours[i], neighbours[j]
                    if w in adjacency[v]:
                        found.add(tuple(sorted([u, v, w])))
    return len(found)


def part_b(data):
    adjacency = parse_data(data)
    best_clique, best_size = set(), 0

    def bron_kerbosch(current_clique, candidates, excluded):
        nonlocal best_clique, best_size
        if not candidates and not excluded:
            if len(current_clique) > best_size:
                best_size = len(current_clique)
                best_clique = current_clique
            return
        if len(current_clique) + len(candidates) <= best_size:
            return
        if candidates:
            pivot, minimum_size = None, float('inf')
            for candidate in candidates:
                size_diff = len(candidates - adjacency[candidate])
                if size_diff < minimum_size:
                    minimum_size = size_diff
                    pivot = candidate
            for vertex in list(candidates - adjacency[pivot]):
                new_clique = current_clique | {vertex}
                new_candidates = candidates & adjacency[vertex]
                new_excluded = excluded & adjacency[vertex]
                bron_kerbosch(new_clique, new_candidates, new_excluded)
                candidates.remove(vertex)
                excluded.add(vertex)

    bron_kerbosch(set(), set(adjacency.keys()), set())
    return ",".join(sorted(best_clique))


def main():
    examples = [
        (
            """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
""",
            7,
            "co,de,ka,ta"
        )
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
