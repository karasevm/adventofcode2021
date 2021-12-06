import sys
import itertools


def coords_to_point_list(a: tuple[int, int], b: tuple[int, int]) -> list[tuple[int, int]]:

    if a[0] == b[0]:   # line is on x axis
        y_list = []
        if a[1] < b[1]:
            y_list = list(range(a[1], b[1]+1))
        else:
            y_list = list(range(b[1], a[1]+1))
        return [(a[0], item) for item in y_list]

    if a[1] == b[1]:   # line is on y axis
        x_list = []
        if a[0] < b[0]:
            x_list = list(range(a[0], b[0]+1))
        else:
            x_list = list(range(b[0], a[0]+1))
        return [(item, a[1]) for item in x_list]
    return []


def coords_to_point_list_diagonals(a: tuple[int, int], b: tuple[int, int]) -> list[tuple[int, int]]:

    y_list = []
    if a[1] < b[1]:
        y_list = list(range(a[1], b[1]+1))
    else:
        y_list = list(range(a[1], b[1]-1, -1))

    x_list = []
    if a[0] < b[0]:
        x_list = list(range(a[0], b[0]+1))
    else:
        x_list = list(range(a[0], b[0]-1, -1))

    return list(zip(x_list, itertools.cycle(y_list)) if len(x_list) > len(y_list) else zip(itertools.cycle(x_list), y_list))


def parse_coords(input_list: list[str]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    result_list = []
    for line in input_list:
        points = line.split(' -> ')
        a = tuple([int(point) for point in points[0].split(',')])
        b = tuple([int(point) for point in points[1].split(',')])
        result_list.append((a, b))
    return result_list


def list_duplicates(coords: list[tuple[tuple[int, int], tuple[int, int]]]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    seen = set()
    duplicates = set()
    for pair in coords:
        if pair in seen:
            duplicates.add(pair)
        else:
            seen.add(pair)
    return list(duplicates)


def part1(input_list: list[str]) -> int:
    coord_pairs = parse_coords(input_list)
    points = []
    for pair in coord_pairs:
        points.extend(coords_to_point_list(pair[0], pair[1]))
    return len(list_duplicates(points))


def part2(input_list: list[str]) -> int:
    coord_pairs = parse_coords(input_list)
    points = []
    for pair in coord_pairs:
        points.extend(coords_to_point_list_diagonals(pair[0], pair[1]))
    return len(list_duplicates(points))


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
