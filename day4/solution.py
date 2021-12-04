import sys
import re


def parse_boards(input_list: list[str]) -> list[list[list[int]]]:
    boards: list[list[list[int]]] = []
    for i in range(1, len(input_list), 6):
        boards.append([[int(item) for item in re.findall(r'[^ ]+', line)]
                      for line in input_list[i+1:i+6]])
    return boards


def list_consists_of_elements(input_list: list[int], elements: list[int]) -> bool:
    for element in input_list:
        if element not in elements:
            return False
    return True


def check_board(board: list[list[int]], numbers: list[int]) -> bool:
    for line in board:
        if list_consists_of_elements(line, numbers):
            return True

    for column in list(zip(*board)):
        if list_consists_of_elements(list(column), numbers):
            return True

    return False


def calculate_board_score(board: list[list[int]], numbers: list[int]) -> int:
    new_board = []
    for line in board:
        new_board.append([x for x in line if x not in numbers])
    return sum([sum(line) for line in new_board]) * numbers[-1]


def part1(input_list: list[str]) -> int:
    numbers = [int(number) for number in input_list[0].split(',')]
    boards = parse_boards(input_list)
    draws_to_win = [sys.maxsize] * len(boards)

    for i in range(len(numbers)):
        for j in range(len(boards)):
            if draws_to_win[j] == sys.maxsize and check_board(boards[j], numbers[:i]):
                draws_to_win[j] = i

    min_board = sys.maxsize
    min_board_index = -1
    for i, draws in enumerate(draws_to_win):
        if draws < min_board:
            min_board = draws
            min_board_index = i

    return calculate_board_score(boards[min_board_index], numbers[:min_board])


def part2(input_list: list[str]) -> int:
    numbers = [int(number) for number in input_list[0].split(',')]
    boards = parse_boards(input_list)
    draws_to_win = [-sys.maxsize] * len(boards)

    for i in range(len(numbers)):
        for j in range(len(boards)):
            if draws_to_win[j] == -sys.maxsize and check_board(boards[j], numbers[:i]):
                draws_to_win[j] = i

    max_board = -sys.maxsize
    max_board_index = -1
    for i, draws in enumerate(draws_to_win):
        if draws > max_board:
            max_board = draws
            max_board_index = i

    return calculate_board_score(boards[max_board_index], numbers[:max_board])


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
