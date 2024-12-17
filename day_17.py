from run_util import run_puzzle


def parse_data(data):
    lines = data.strip().split('\n')
    a = int(lines[0].split(':')[1].strip())
    b = int(lines[1].split(':')[1].strip())
    c = int(lines[2].split(':')[1].strip())
    program_str = lines[4].split(':')[1].strip()
    program = list(map(int, program_str.split(',')))
    return a, b, c, program


def run_program(a, b, c, program):
    def combo_value(operand, a, b, c):
        if operand <= 3:
            return operand
        elif operand == 4:
            return a
        elif operand == 5:
            return b
        elif operand == 6:
            return c

    ip = 0
    out = []
    while ip + 1 < len(program):

        opcode = program[ip]
        op = program[ip + 1]

        match opcode:
            case 0:
                a = a // (2 ** combo_value(op, a, b, c))
            case 1:
                b = b ^ op
            case 2:
                b = combo_value(op, a, b, c) % 8
            case 3:
                if a != 0:
                    ip = op - 2
            case 4:
                b = b ^ c
            case 5:
                out.append(combo_value(op, a, b, c) % 8)
            case 6:
                b = a // (2 ** combo_value(op, a, b, c))
            case 7:
                c = a // (2 ** combo_value(op, a, b, c))

        ip += 2
    return out


def part_a(data):
    a, b, c, program = parse_data(data)
    out = run_program(a, b, c, program)
    return ','.join(map(str, out))


def find_quine(program):
    stack = [(len(program) - 1, 0, 0)]
    while stack:
        i, acc_a, candidate_start = stack.pop()
        for candidate in range(candidate_start, 8):
            a = acc_a * 8 + candidate
            result = run_program(a, 0, 0, program)
            if result == program[i:]:
                if i == 0:
                    return a
                stack.append((i, acc_a, candidate + 1))
                stack.append((i - 1, a, 0))
                break


def part_b(data):
    _, _, _, program = parse_data(data)
    return find_quine(program)


def main():
    examples = [
        ("""Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0""", "4,6,3,5,6,3,5,2,1,0", None)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
