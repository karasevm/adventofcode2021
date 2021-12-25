import sys


def part1(input_list: list[str]) -> int:
    cucumber_map = [[char for char in line] for line in input_list]
    new_cucumber_map = []
    iter_count = 0
    changed = True
    while changed:
        changed = False
        iter_count += 1
        new_cucumber_map = [
            ['.' for _ in range(len(cucumber_map[0]))] for _ in range(len(cucumber_map))]
        for row, line in enumerate(cucumber_map):
            for col, char in enumerate(line):
                next_col = (col+1) % len(cucumber_map[0])
                if char == '>' and line[next_col] == '.':
                    new_cucumber_map[row][col] = '.'
                    new_cucumber_map[row][next_col] = '>'
                    changed = True
                elif char != '.':
                    new_cucumber_map[row][col] = char
        cucumber_map = new_cucumber_map

        new_cucumber_map = [
            ['.' for _ in range(len(cucumber_map[0]))] for _ in range(len(cucumber_map))]
        for row, line in enumerate(cucumber_map):
            for col, char in enumerate(line):
                next_row = (row+1) % len(cucumber_map)
                if char == 'v' and cucumber_map[next_row][col] == '.':
                    new_cucumber_map[row][col] = '.'
                    new_cucumber_map[next_row][col] = 'v'
                    changed = True
                elif char != '.':
                    new_cucumber_map[row][col] = char
        cucumber_map = new_cucumber_map
    return iter_count


def part2(input_list: list[str]) -> int:
    return 0


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
