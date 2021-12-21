import sys
from functools import reduce
import itertools
from typing import Union
import math


def reduce(line: str) -> str:
    line_list: list[Union[int, str]] = []
    i = 0
    while i < len(line):
        if line[i] in ["[", "]", ","]:
            line_list.append(line[i])
            i += 1
            continue
        int_string = ""
        while line[i] not in ["[", "]", ","]:
            int_string += line[i]
            i += 1
        line_list.append(int(int_string))

    new_line = []
    explosion_line = []
    split_line = []
    while new_line != line_list:
        new_line = [el for el in line_list]

        while explosion_line != line_list:
            explosion_line = [el for el in line_list]
            depth = 0
            for index, char in enumerate(line_list):
                if char == "[":
                    depth += 1
                elif char == "]":
                    depth -= 1
                elif depth > 4:  # explode
                    numbers: list[int] = []

                    for subindex, subchar in enumerate(line_list[index:]):
                        if subchar == "]":
                            numbers = [x[0] for x in [list(y) for x, y in itertools.groupby(
                                line_list[index:index+subindex], lambda z: z == ',') if not x]]  # type: ignore
                            # replace the group with zero
                            line_list = line_list[:index-1] + \
                                [0] + line_list[index+subindex+1:]
                            # print(numbers, " "*index,"^"*subindex)
                            break

                    for i in range(index-2, -1, -1):
                        if line_list[i] not in ["[", "]", ","]:
                            line_list[i] = line_list[i] + \
                                numbers[0]  # type: ignore
                            break
                    for i in range(index, len(line_list)):
                        if line_list[i] not in ["[", "]", ","]:
                            line_list[i] = line_list[i] + \
                                numbers[1]  # type: ignore
                            break
                    break

        for index, char in enumerate(line_list):
            if line_list[index] not in ["[", "]", ","]:
                if line_list[index] >= 10:  # type: ignore
                    line_list[index:index+1] = ["[", math.floor(
                        line_list[index]/2), ",", math.ceil(line_list[index]/2), "]"]  # type: ignore
                    # print("        ", " "*(index-2),"^^")
                    # print("split  ", ''.join([str(el) for el in line_list]))
                    break

    return ''.join([str(el) for el in line_list])


def sf_sum(num1: str, num2: str) -> str:
    return "[" + num1 + "," + num2 + "]"


def calc_magnitude(line: str) -> int:
    line_list: list[Union[int, str]] = []

    for char in line:
        if char in ["[", "]", ","]:
            line_list.append(char)
        else:
            line_list.append(int(char))

    while len(line_list) != 1:
        new_line = []
        i = 0
        while i < len(line_list):
            if line_list[i] == "[" and line_list[i+2] == "," and line_list[i+4] == "]":

                new_line.append(line_list[i+1]*3 +
                                line_list[i+3]*2)  # type: ignore
                i += 5
            else:
                new_line.append(line_list[i])
                i += 1

        line_list = new_line
    return line_list[0]  # type: ignore


def part1(input_list: list[str]) -> int:
    previous_result = reduce(input_list[0])
    for line in input_list[1:]:
        line = reduce(line)
        previous_result = reduce(sf_sum(previous_result, line))
    return calc_magnitude(previous_result)


def part2(input_list: list[str]) -> int:
    max_sum = 0
    for line_a in input_list:
        for line_b in input_list:
            if line_a == line_b:
                continue
            current_sum = calc_magnitude(
                reduce(sf_sum(reduce(line_a), reduce(line_b))))
            if current_sum > max_sum:
                max_sum = current_sum

    return max_sum


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
