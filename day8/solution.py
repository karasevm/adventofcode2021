import sys
from collections import Counter


def part1(input_list: list[str]) -> int:
    output_digits: list[list[str]] = [item[1].split(
        ' ') for item in [line.split(' | ') for line in input_list]]
    acceptable_lengths = [2, 3, 4, 7]
    result = 0
    for line in output_digits:
        for digit in line:
            if len(digit) in acceptable_lengths:
                result += 1
    return result


def part2(input_list: list[str]) -> int:
    digits: list[list[str]] = [item[0].split(
        ' ') for item in [line.split(' | ') for line in input_list]]
    output_digits: list[list[str]] = [item[1].split(
        ' ') for item in [line.split(' | ') for line in input_list]]
    wire_digit_map = {'ABCEFG': 0, 'CF': 1, 'ACDEG': 2, 'ACDFG': 3,
                      'BCDF': 4, 'ABDFG': 5, 'ABDEFG': 6, 'ACF': 7, 'ABCDEFG': 8, 'ABCDFG': 9}
    result = 0
    for line in range(len(digits)):
        wire_map = {'A': 'z', 'B': 'z', 'C': 'z',
                    'D': 'z', 'E': 'z', 'F': 'z', 'G': 'z'}
        A_candidates = []
        G_candidates = []
        counts = Counter(''.join(digits[line])).items()
        for k, v in counts:
            if v == 6:
                wire_map['B'] = k
            elif v == 4:
                wire_map['E'] = k
            elif v == 7:
                G_candidates.append(k)
            elif v == 8:
                A_candidates.append(k)
            elif v == 9:
                wire_map['F'] = k
        digit_map: dict[str, list[str]] = {}
        for digit in digits[line]:
            if len(digit) == 2:
                digit_map['1'] = sorted(digit)
            elif len(digit) == 3:
                digit_map['7'] = sorted(digit)
            elif len(digit) == 4:
                digit_map['4'] = sorted(digit)
            elif len(digit) == 7:
                digit_map['8'] = sorted(digit)
        wire_map['C'] = (set(digit_map['1']) -
                         set([char for char in wire_map['F']])).pop()
        wire_map['D'] = (set(digit_map['4']) -
                         set(digit_map['1']) -
                         set(wire_map['B'])).pop()
        wire_map['A'] = (set(A_candidates) - set(wire_map['C'])).pop()
        wire_map['G'] = (set(G_candidates) - set(wire_map['D'])).pop()

        inverse_wire_map = {v: k for k, v in wire_map.items()}
        new_output: list[str] = []
        for digit in output_digits[line]:
            new_digit = ''
            for char in digit:
                new_digit = new_digit + inverse_wire_map[char]
            new_output.append(''.join(sorted(new_digit)))

        numeric_result = 0
        for digit in new_output:
            numeric_result *= 10
            numeric_result += wire_digit_map[digit]
        result += numeric_result

    return result


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
