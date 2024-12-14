from run_util import run_puzzle


def parse_data(data):
    robots = []
    for line in data.strip().split('\n'):
        if not line.strip():
            continue
        p_part, v_part = line.split()
        x_str = p_part.split('=')[1]
        dx_str = v_part.split('=')[1]
        x, y = map(int, x_str.split(','))
        dx, dy = map(int, dx_str.split(','))
        robots.append((x, y, dx, dy))
    return robots


def part_a(data):
    robots = parse_data(data)
    if len(robots) == 12:

        width, height = 11, 7
    else:
        width, height = 101, 103

    time = 100

    final_positions = []
    for x, y, dx, dy in robots:
        final_x = (x + dx * time) % width
        final_y = (y + dy * time) % height
        final_positions.append((final_x, final_y))

    mid_x = width // 2
    mid_y = height // 2

    q_tl = q_tr = q_bl = q_br = 0
    for (fx, fy) in final_positions:
        if fx < mid_x and fy < mid_y:
            q_tl += 1
        elif fx > mid_x and fy < mid_y:
            q_tr += 1
        elif fx < mid_x and fy > mid_y:
            q_bl += 1
        elif fx > mid_x and fy > mid_y:
            q_br += 1

    safety_factor = q_tl * q_tr * q_bl * q_br
    return safety_factor


def part_b(data):
    robots = parse_data(data)
    width, height = 101, 103

    total_robots = len(robots)

    time = 0
    positions = set()
    while len(set(positions)) != total_robots:
        time += 1
        positions = set()
        for x, y, dx, dy in robots:
            fx = (x + dx * time) % width
            fy = (y + dy * time) % height
            positions.add((fx, fy))

    return time


def main():
    examples = [
        ("""p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3""", 12, None)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
