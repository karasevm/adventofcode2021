import sys
from collections import defaultdict


def get_pixel(zone: str, lut: str) -> str:
    index = 0
    for i, val in enumerate(zone[::-1]):
        if val == "#":
            index += 2**i
    return lut[index]


def process_image(image: defaultdict[tuple[int, int], str], lut: str, iterations: int, size: int) -> int:
    min_row = -10
    min_col = -10
    max_row = size + 10
    max_col = size + 10

    count = 0
    for _ in range(iterations+1):
        new_image = defaultdict(lambda: '.')
        count = 0
        for row in range(min_row, max_row):
            for col in range(min_col, max_col):
                # make next image
                zone = ''
                for drow in range(-1, 2):
                    for dcol in range(-1, 2):
                        zone += image[(row+drow, col+dcol)]
                new_image[(row, col)] = get_pixel(zone, lut)

                # print current image
                if image[(row, col)] == "#":
                    count += 1
                # print(image[(row,col)], end="")

        image = new_image
        if new_image[(min_row, min_col)] == "#":
            image.default_factory = lambda: '#'

        else:
            image.default_factory = lambda: '.'
        min_row -= 1
        min_col -= 1
        max_col += 1
        max_row += 1

    return count


def part1(input_list: list[str]) -> int:
    lut = input_list[0]
    image: defaultdict[tuple[int, int], str] = defaultdict(lambda: '.')

    for row, line in enumerate(input_list[2:]):
        for col, char in enumerate(line):
            image[(row, col)] = char

    return process_image(image, lut, 2, len(input_list[3]))


def part2(input_list: list[str]) -> int:
    lut = input_list[0]
    image: defaultdict[tuple[int, int], str] = defaultdict(lambda: '.')

    for row, line in enumerate(input_list[2:]):
        for col, char in enumerate(line):
            image[(row, col)] = char

    return process_image(image, lut, 50, len(input_list[3]))


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
