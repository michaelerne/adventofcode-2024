from run_util import run_puzzle


def parse_data(data):
    lines = [l for l in data.strip().split('\n') if l]
    robots = []
    for line in lines:
        p_part, v_part = line.split()
        x, y = map(int, p_part[2:].split(','))
        dx, dy = map(int, v_part[2:].split(','))
        robots.append((x, y, dx, dy))
    return robots


def minimal_arc_length(coords, length):
    coords.sort()
    n = len(coords)
    extended = coords + [c + length for c in coords]
    return min(extended[i + n - 1] - extended[i] for i in range(n))


def clustering_time(base, length):
    return min(
        range(length),
        key=lambda t: minimal_arc_length([(p + v * t) % length for p, v in base], length)
    )


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

    t_x = clustering_time([(r[0], r[2]) for r in robots], width)
    t_y = clustering_time([(r[1], r[3]) for r in robots], height)

    diff = (t_y - t_x) % height
    a = diff * 51 % height
    ttCt = width * a + t_x  # time to Christmas tree

    return ttCt


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
