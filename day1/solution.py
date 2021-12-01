import sys


def part1(input_list: list[int]) -> int:
    output = 0
    for i in range(1, len(input_list)):
        if input_list[i] > input_list[i-1]:
            output += 1
    return output


def part2(input_list: list[int]) -> int:
    output = 0
    for i in range(4, len(input_list)+1):
        if sum(input_list[i-4:i-1]) < sum(input_list[i-3:i]):
            output += 1
    return output

if __name__ == "__main__":
    try:
        f = open(sys.argv[1], "r")
    except IOError:
        print("Error opening the file, try again")
        sys.exit(1)
    with f:
        lines = f.readlines()
        f.close()
        digits = [int(s) for s in lines]
        print(
        f"Part 1 answer:{part1(digits)} Part 2 answer: {part2(digits)}")
