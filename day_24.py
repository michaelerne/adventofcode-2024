from collections import defaultdict, deque

from run_util import run_puzzle


def parse_data(data):
    lines = [line.strip() for line in data.strip().splitlines() if line.strip()]

    wire_values = {}
    gates = []

    for line in lines:
        if "->" in line:
            left_part, out_wire = line.split("->")
            parts = left_part.strip().split()
            inp_a, gate_op, inp_b = parts
            gates.append((inp_a, gate_op, inp_b, out_wire.strip()))
        else:
            wire_name, val_str = line.split(":")
            wire_values[wire_name.strip()] = int(val_str.strip())

    return wire_values, gates


def evaluate_gates(wire_values, gates):
    adjacency = defaultdict(list)
    in_degree = [2] * len(gates)

    for i, (input_a, gate_operation, input_b, output_wire) in enumerate(gates):
        adjacency[input_a].append(i)
        adjacency[input_b].append(i)

    ready = deque()

    def reduce_in_degree(gate_idx):
        nonlocal in_degree, ready
        in_degree[gate_idx] -= 1
        if in_degree[gate_idx] == 0:
            ready.append(gate_idx)

    for known_wire in wire_values:
        if known_wire in adjacency:
            for gate_index in adjacency[known_wire]:
                reduce_in_degree(gate_index)

    while ready:
        gate_index = ready.popleft()
        input_a, gate_operation, input_b, output_wire = gates[gate_index]

        if input_a not in wire_values or input_b not in wire_values:
            continue

        value_a = wire_values[input_a]
        value_b = wire_values[input_b]

        if gate_operation == 'AND':
            output_value = value_a & value_b
        elif gate_operation == 'OR':
            output_value = value_a | value_b
        elif gate_operation == 'XOR':
            output_value = value_a ^ value_b

        if output_wire not in wire_values:
            wire_values[output_wire] = output_value
            if output_wire in adjacency:
                for next_gate in adjacency[output_wire]:
                    reduce_in_degree(next_gate)

    return wire_values


def part_a(data):
    wire_values, gates = parse_data(data)
    wire_values = evaluate_gates(wire_values, gates)
    z_list = [(int(w[1:]), val) for w, val in wire_values.items() if w.startswith('z')]
    bits = [str(bit_val) for (_idx, bit_val) in sorted(z_list, key=lambda x: x[0])]
    return int(''.join(reversed(bits)), 2)


def find_gate_output(gates, name_a, name_b, gate_op):
    for (left_in, op, right_in, out_w) in gates:
        if op == gate_op and {left_in, right_in} == {name_a, name_b}:
            return out_w


def swap_wires(gates):
    swapped_wires = []
    carry_in = None

    for i in range(45):
        idx_str = str(i).zfill(2)
        xor_wire = find_gate_output(gates, f"x{idx_str}", f"y{idx_str}", 'XOR')
        and_wire = find_gate_output(gates, f"x{idx_str}", f"y{idx_str}", 'AND')

        if carry_in:
            r_wire = find_gate_output(gates, carry_in, xor_wire, 'AND')
            if not r_wire:
                xor_wire, and_wire = and_wire, xor_wire
                swapped_wires.extend([xor_wire, and_wire])
                r_wire = find_gate_output(gates, carry_in, xor_wire, 'AND')

            sum_wire = find_gate_output(gates, carry_in, xor_wire, 'XOR')

            if xor_wire and xor_wire.startswith('z'):
                xor_wire, sum_wire = sum_wire, xor_wire
                swapped_wires.extend([xor_wire, sum_wire])

            if and_wire and and_wire.startswith('z'):
                and_wire, sum_wire = sum_wire, and_wire
                swapped_wires.extend([and_wire, sum_wire])

            if r_wire and r_wire.startswith('z'):
                r_wire, sum_wire = sum_wire, r_wire
                swapped_wires.extend([r_wire, sum_wire])

            c_out_wire = find_gate_output(gates, r_wire, and_wire, 'OR')

            if c_out_wire and c_out_wire.startswith('z') and c_out_wire != 'z45':
                c_out_wire, sum_wire = sum_wire, c_out_wire
                swapped_wires.extend([c_out_wire, sum_wire])

            carry_in = c_out_wire if carry_in else and_wire
        else:
            carry_in = and_wire

    return swapped_wires


def part_b(data):
    wire_values, gates = parse_data(data)
    evaluate_gates(wire_values, gates)
    swaps = swap_wires(gates)
    return ",".join(sorted(swaps))


def main():
    examples = []
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
