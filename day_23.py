import networkx as nx

from run_util import run_puzzle


def parse_data(data):
    return nx.Graph([x.split('-') for x in data.strip().split('\n')])


def part_a(data):
    graph = parse_data(data)

    return sum(
        1
        for clique in nx.enumerate_all_cliques(graph)
        if len(clique) == 3 and any(node.startswith('t') for node in clique)
    )


def part_b(data):
    graph = parse_data(data)

    return ','.join(sorted(max(nx.find_cliques(graph), key=len)))


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
