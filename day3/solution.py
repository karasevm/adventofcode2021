import sys


def part1(input_list: list[str]) -> int:
    input_list_len = len(input_list)
    rotated_list = list(zip(*input_list[::-1]))
    rotated_list_len = len(rotated_list)
    result_gamma = 0

    for bit in rotated_list:
        result_gamma = result_gamma << 1
        if sum(map(int, bit)) > input_list_len // 2:
            result_gamma = result_gamma | 1

    return result_gamma * (~result_gamma & ((1 << rotated_list_len) - 1))


def count_ones_in_column(input_m: list[str], column: int) -> int:
    total = 0
    for row in input_m:
        if row[column] == "1":
            total += 1
    return total


def part2(input_list: list[str]) -> int:

    new_list = input_list.copy()
    i = 0
    while len(new_list) != 1:
        if count_ones_in_column(new_list, i) >= len(new_list) / 2:
            new_list = [entry for entry in new_list if entry[i] == '1']
        else:
            new_list = [entry for entry in new_list if entry[i] == '0']
        i += 1
    result_oxygen = int(new_list[0], 2)

    new_list = input_list.copy()
    i = 0
    while len(new_list) != 1:
        if count_ones_in_column(new_list, i) < len(new_list) / 2:
            new_list = [entry for entry in new_list if entry[i] == '1']
        else:
            new_list = [entry for entry in new_list if entry[i] == '0']
        i += 1
    result_co2 = int(new_list[0], 2)

    return result_oxygen * result_co2


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
