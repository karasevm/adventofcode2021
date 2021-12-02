import sys


def part1(input_list: list[str]) -> int:
    pos_x = 0
    pos_y = 0
    for input_command in input_list:
        inputs = input_command.split(" ")
        match inputs[0]:
            case 'forward':
                pos_x += int(inputs[1])
            case 'down':
                pos_y += int(inputs[1])
            case 'up':
                pos_y -= int(inputs[1])

    return pos_x * pos_y


def part2(input_list: list[str]) -> int:
    pos_x = 0
    pos_y = 0
    aim = 0
    for input_command in input_list:
        inputs = input_command.split(" ")
        match inputs[0]:
            case 'forward':
                pos_x += int(inputs[1])
                pos_y += aim * int(inputs[1])
            case 'down':
                aim += int(inputs[1])
            case 'up':
                aim -= int(inputs[1])

    return pos_x * pos_y


if __name__ == "__main__":
    try:
        f = open(sys.argv[1], "r")
    except IOError:
        print("Error opening the file, try again")
        sys.exit(1)
    with f:
        lines = f.readlines()
        f.close()
        print(
            f"Part 1 answer:{part1(lines)} Part 2 answer: {part2(lines)}")
