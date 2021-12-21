import sys
import re


def does_hit_target(velocity: tuple[int, int], target_x: tuple[int, int], target_y: tuple[int, int]) -> tuple[bool, int]:
    x = 0
    y = 0
    dx = velocity[0]
    dy = -velocity[1]
    highest_y = sys.maxsize
    touched_coords = [(int(x), int(y))]

    while x <= target_x[1] and y <= target_y[1]:
        if x >= target_x[0] and y >= target_y[0]:

            # print(touched_coords)
            # for yt in range(highest_y, target_y[1]+1):
            #     for xt in range(target_x[1]+1):
            #         if (xt,yt) in touched_coords:
            #             print("█",end="")
            #         elif xt >= target_x[0] and xt <= target_x[1] and yt <= target_y[1]  and yt >= target_y[0]:
            #             print("▓",end="")
            #         else:
            #             print("░", end="")
            #     print()

            return True, highest_y
        x += dx
        if dx > 0:
            dx -= 1

        y += dy
        if y < highest_y:
            highest_y = y
        dy += 1

        touched_coords.append((x, y))
    return False, highest_y


def part1(input_list: list[str]) -> int:
    coords = [int(x) for x in re.findall("\\-?\\d+", input_list[0])]
    coords[2], coords[3] = -coords[3], -coords[2]
    does_hit_target((7, 2), (coords[0], coords[1]), (coords[2], coords[3]))
    result = sys.maxsize
    for y in range(500):
        for x in range(500):
            t, ym = does_hit_target(
                (x, y), (coords[0], coords[1]), (coords[2], coords[3]))
            if t:
                if ym < result:
                    result = ym
        for x in range(500):
            t, ym = does_hit_target(
                (x, -y), (coords[0], coords[1]), (coords[2], coords[3]))
            if t:
                if ym < result:
                    result = ym

    return -result


def part2(input_list: list[str]) -> int:
    coords = [int(x) for x in re.findall("\\-?\\d+", input_list[0])]
    coords[2], coords[3] = -coords[3], -coords[2]
    does_hit_target((7, 2), (coords[0], coords[1]), (coords[2], coords[3]))
    result = set()
    for y in range(500):
        for x in range(500):
            t, ym = does_hit_target(
                (x, y), (coords[0], coords[1]), (coords[2], coords[3]))
            if t:
                result.add((x, y))
        for x in range(500):
            t, ym = does_hit_target(
                (x, -y), (coords[0], coords[1]), (coords[2], coords[3]))
            if t:
                result.add((x, -y))

    return len(result)


if __name__ == "__main__":
    try:
        f = open(sys.argv[1], "r")
    except IOError:
        print("Error opening the file, try again")
        sys.exit(1)
    with f:
        lines = f.readlines()
        lines = [line.rstrip() for line in lines]
        f.close()
        print(
            f"Part 1 answer: {part1(lines)} Part 2 answer: {part2(lines)}")
