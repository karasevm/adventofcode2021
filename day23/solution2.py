
from collections import defaultdict, deque
import sys
from queue import PriorityQueue


class Diagram:
    def __init__(self, dg: list[list[str]], cost: int = 0):
        self.dg = dg
        self.cost = cost

    def get_copy(self):
        return Diagram([line[:] for line in self.dg], self.cost)

    def __hash__(self):
        return hash(self.dg_fingerprint())

    def __eq__(self, other):
        return self.dg_fingerprint() == other.dg_fingerprint()

    def is_sorted(self):
        if len(self.dg) == 5:
            return ''.join(self.dg[2]) == "###A#B#C#D###" and ''.join(self.dg[3]) == "  #A#B#C#D#"
        if len(self.dg) == 7:
            return ''.join(self.dg[2]) == "###A#B#C#D###" and ''.join(self.dg[3]) == "  #A#B#C#D#" and ''.join(self.dg[4]) == "  #A#B#C#D#" and ''.join(self.dg[5]) == "  #A#B#C#D#"

    def __lt__(self, other):
        return self.cost < other.cost

    def print(self):
        for line in self.dg:
            print(''.join(line))

    def dg_fingerprint(self):
        return ''.join([''.join(x) for x in self.dg])


def can_pathfind(diagram: Diagram, point_a: tuple[int, int], point_b: tuple[int, int]) -> tuple[bool, int]:
    to_check = deque()
    to_check.append((0, point_a))
    visited = set()
    while to_check:
        path, coords = to_check.popleft()
        if coords in visited:
            continue
        visited.add(coords)
        if coords == point_b:
            return True, path
        for offset_row, offset_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if diagram.dg[coords[0]+offset_row][coords[1]+offset_col] == '.':
                to_check.append(
                    (path+1, (coords[0]+offset_row, coords[1]+offset_col)))
    return False, 0


def check_room(diagram: Diagram, coords: tuple[int, int]) -> bool:
    room_map = {"A": 3, "B": 5, "C": 7, "D": 9}
    col_char = diagram.dg[coords[0]][coords[1]]
    if col_char not in room_map.keys():
        return False
    if coords[1] != room_map[col_char]:
        return False
    for row in range(coords[0], len(diagram.dg)-1):
        if diagram.dg[row][coords[1]] != col_char:
            return False
    return True


def find_possible_moves(diagram: Diagram) -> list[Diagram]:
    results = []
    for row, line in enumerate(diagram.dg):
        for column, char in enumerate(line):
            if char in ["A", "B", "C", "D"]:
                if check_room(diagram, (row, column)):
                    continue

                cost = 1
                match char:
                    case 'B':
                        cost *= 10
                    case 'C':
                        cost *= 100
                    case 'D':
                        cost *= 1000

                if row > 1:  # inside a room
                    for position in [1, 2, 4, 6, 8, 10, 11]:
                        possible, path_length = can_pathfind(
                            diagram, (row, column), (1, position))
                        if possible:
                            new_diagram = diagram.get_copy()
                            new_diagram.dg[1][position] = new_diagram.dg[row][column]
                            new_diagram.dg[row][column] = '.'
                            new_diagram.cost += path_length * cost
                            results.append(new_diagram)

                room_map = {"A": 3, "B": 5, "C": 7, "D": 9}
                if row == 1:  # in the hallway
                    for position in range(len(diagram.dg) - 2, 1, -1):
                        possible, path_length = can_pathfind(
                            diagram, (row, column), (position, room_map[char]))
                        if possible and (position == len(diagram.dg) - 2 or check_room(diagram, (position + 1, room_map[char]))):
                            new_diagram = diagram.get_copy()
                            new_diagram.dg[position][room_map[char]
                                                     ] = new_diagram.dg[row][column]
                            new_diagram.dg[row][column] = '.'
                            new_diagram.cost += path_length * cost
                            results.append(new_diagram)
                            break

    return results


def part1(input_list: list[str]) -> int:
    input_diagram = Diagram([list(x) for x in input_list])

    print(input_diagram.is_sorted())
    visited = defaultdict(lambda: sys.maxsize)
    diagrams_to_check: PriorityQueue[Diagram] = PriorityQueue()
    diagrams_to_check.put(input_diagram)
    count = 0
    skip_count = 0
    while not diagrams_to_check.empty():

        current_dg = diagrams_to_check.get()
        count += 1
        if count % 500 == 0:
            print("checked", count, "skipped", skip_count, "in queue",
                  diagrams_to_check.qsize(), "current cost", current_dg.cost)
        if current_dg.is_sorted():
            print("Solved")
            current_dg.print()
            print()
            print(current_dg.cost)
            return current_dg.cost
        new_dgs = find_possible_moves(current_dg)
        for dg in new_dgs:
            if dg.cost < visited[dg.dg_fingerprint()]:
                visited[dg.dg_fingerprint()] = dg.cost
                diagrams_to_check.put(dg)
            else:
                skip_count += 1

    return 0


def part2(input_list: list[str]) -> int:
    input_list.insert(3, "  #D#C#B#A#")
    input_list.insert(4, "  #D#B#A#C#")
    for line in input_list:
        print(line)
    input_diagram = Diagram([list(x) for x in input_list])

    print(input_diagram.is_sorted())
    visited = defaultdict(lambda: sys.maxsize)
    diagrams_to_check: PriorityQueue[Diagram] = PriorityQueue()
    diagrams_to_check.put(input_diagram)
    count = 0
    skip_count = 0
    while not diagrams_to_check.empty():

        current_dg = diagrams_to_check.get()
        count += 1
        if count % 500 == 0:
            print("checked", count, "skipped", skip_count, "in queue",
                  diagrams_to_check.qsize(), "current cost", current_dg.cost)
        if current_dg.is_sorted():
            print("Solved")
            current_dg.print()
            print()
            print(current_dg.cost)
            return current_dg.cost
        new_dgs = find_possible_moves(current_dg)
        for dg in new_dgs:
            if dg.cost < visited[hash(dg)]:
                visited[hash(dg)] = dg.cost
                diagrams_to_check.put(dg)
            else:
                skip_count += 1

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
