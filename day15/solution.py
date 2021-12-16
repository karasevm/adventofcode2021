import sys
from queue import PriorityQueue


def min_cost(danger_map: list[list[int]]) -> int:

    visited = set()
    to_visit = PriorityQueue()

    to_visit.put((0, 0, 0))

    while not to_visit.empty():
        cost, line, number = to_visit.get()
        if (line, number) in visited:
            continue
        visited.add((line, number))

        if line != 0:
            to_visit.put((cost+danger_map[line-1][number], line-1, number))
        if number != 0:
            to_visit.put((cost+danger_map[line][number-1], line, number-1))
        if number != len(danger_map[0])-1:
            to_visit.put((cost+danger_map[line][number+1], line, number+1))
        if line != len(danger_map)-1:
            to_visit.put((cost+danger_map[line+1][number], line+1, number))

        if line == len(danger_map) - 1 and number == len(danger_map) - 1:
            return cost

    return 0


def part1(input_list: list[str]) -> int:
    map = [[int(item) for item in line] for line in input_list]
    return min_cost(map)


def part2(input_list: list[str]) -> int:
    map = [[int(item) for item in line] for line in input_list]

    expanded_map = []
    for repeat_line in range(5):
        for line in map:
            new_line = []
            for repeat_number in range(5):
                for number in line:
                    new_number = number + repeat_number + repeat_line
                    if new_number >= 10:
                        new_number -= 9
                    new_line.append(new_number)
            expanded_map.append(new_line)

    return min_cost(expanded_map)


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
