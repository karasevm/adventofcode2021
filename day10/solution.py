import sys
from collections import deque


def part1(input_list: list[str]) -> int:
    bracket_map = {"(": ")", "[": "]", "{": "}", "<": ">"}
    point_map = {")": 3, "]": 57, "}": 1197, ">": 25137}
    result = 0
    for line in input_list:
        brackets = deque()
        for char in line:
            if char in ["(", "[", "{", "<"]:
                brackets.append(char)
            else:
                expected_bracket = bracket_map[brackets.pop()]
                if char != expected_bracket:
                    result += point_map[char]
                    continue

    return result


def part2(input_list: list[str]) -> int:
    bracket_map = {"(": ")", "[": "]", "{": "}", "<": ">"}
    point_map = {")": 1, "]": 2, "}": 3, ">": 4}
    results = []
    for line in input_list:
        brackets = deque()
        for i, char in enumerate(line):
            if char in ["(", "[", "{", "<"]:
                brackets.append(char)
            else:
                expected_bracket = bracket_map[brackets.pop()]
                if char != expected_bracket:
                    break

            if i == len(line) - 1:
                line_result = 0
                while brackets:
                    expected_bracket = bracket_map[brackets.pop()]
                    line_result *= 5
                    line_result += point_map[expected_bracket]
                results.append(line_result)

    return sorted(results)[len(results)//2]


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
