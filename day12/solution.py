import sys
from collections import deque


def part1(input_list: list[str]) -> int:
    paths = [["start"]]
    result_paths = []
    while True:
        new_paths = []
        added_paths = 0
        for path in paths:
            for line in input_list:
                caves = line.split('-')
                if (caves[0] != 'end' and 
                    caves[0] == path[-1] and 
                    ((caves[1].isupper()) or (caves[1].islower() and caves[1] not in path))):
                    new_paths.append(path + [caves[1]])
                    added_paths += 1
                if (caves[1] != 'end' and 
                    caves[1] == path[-1] and 
                    ((caves[0].isupper()) or (caves[0].islower() and caves[0] not in path))):
                    new_paths.append(path + [caves[0]])
                    added_paths += 1
        result_paths.extend(list(filter(lambda x: x[-1] == 'end', paths)))
        if added_paths == 0:
            break
        else:
            paths = new_paths
    result_paths = list(filter(lambda x: x[-1] == 'end', result_paths))
    return len(result_paths)


def did_visit_small_cave_twice(line: list[str]) -> bool:
    caves = list(filter(lambda x: x.islower(), line))
    return len(set(caves)) != len(caves)


def part2(input_list: list[str]) -> int:
    paths = [["start"]]
    result_paths = []
    while True:
        new_paths = []
        added_paths = 0
        for path in paths:
            for line in input_list:
                caves = line.split('-')
                if (caves[0] != 'end' and 
                    caves[1] != 'start' and 
                    caves[0] == path[-1] and 
                    ((caves[1].isupper()) or (caves[1].islower() and (not did_visit_small_cave_twice(path) or caves[1] not in path)))):
                    new_paths.append(path + [caves[1]])
                    added_paths += 1
                if (caves[1] != 'end' and 
                    caves[0] != 'start' and 
                    caves[1] == path[-1] and 
                    ((caves[0].isupper()) or (caves[0].islower() and (not did_visit_small_cave_twice(path) or caves[0] not in path)))):
                    new_paths.append(path + [caves[0]])
                    added_paths += 1
        result_paths.extend(list(filter(lambda x: x[-1] == 'end', paths)))
        if added_paths == 0:
            break
        else:
            paths = new_paths
    result_paths = list(filter(lambda x: x[-1] == 'end', result_paths))
    # for path in paths:
    #     ''.join(print(path))
    return len(result_paths)


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
