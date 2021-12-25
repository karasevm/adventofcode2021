
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
        # return hash(self)


def can_go_into_column(diagram: Diagram, column: str):
    room_map = {"A": 3, "B": 5, "C": 7, "D": 9}
    for row in diagram.dg[1:-1]:
        if row[room_map[column]] not in [column, '.']:
            return False
    return True


def find_possible_moves(diagram: Diagram, part: int = 1) -> list[Diagram]:
    results = []
    for row, line in enumerate(diagram.dg):
        for column, char in enumerate(line):
            if char in ["A", "B", "C", "D"]:
                if part == 1:
                    if ((char == "A" and (row, column) == (3, 3)) or
                        (char == "B" and (row, column) == (3, 5)) or
                        (char == "C" and (row, column) == (3, 7)) or
                            (char == "D" and (row, column) == (3, 9))):
                        continue

                    if ((char == "A" and (row, column) == (2, 3) and diagram.dg[3][3] == "A") or
                        (char == "B" and (row, column) == (2, 5) and diagram.dg[3][5] == "B") or
                        (char == "C" and (row, column) == (2, 7) and diagram.dg[3][7] == "C") or
                            (char == "D" and (row, column) == (2, 9) and diagram.dg[3][9] == "D")):
                        continue
                else:
                    if ((char == "A" and (row, column) == (5, 3)) or
                        (char == "B" and (row, column) == (5, 5)) or
                        (char == "C" and (row, column) == (5, 7)) or
                            (char == "D" and (row, column) == (5, 9))):
                        continue

                    if ((char == "A" and (row, column) == (4, 3) and diagram.dg[5][3] == "A") or
                        (char == "B" and (row, column) == (4, 5) and diagram.dg[5][5] == "B") or
                        (char == "C" and (row, column) == (4, 7) and diagram.dg[5][7] == "C") or
                            (char == "D" and (row, column) == (4, 9) and diagram.dg[5][9] == "D")):
                        continue

                    if ((char == "A" and (row, column) == (3, 3) and diagram.dg[4][3] == "A" and diagram.dg[5][3] == "A") or
                        (char == "B" and (row, column) == (3, 5) and diagram.dg[4][5] == "B" and diagram.dg[5][5] == "B") or
                        (char == "C" and (row, column) == (3, 7) and diagram.dg[4][7] == "C" and diagram.dg[5][7] == "C") or
                            (char == "D" and (row, column) == (3, 9) and diagram.dg[4][9] == "D" and diagram.dg[5][9] == "D")):
                        continue

                    if ((char == "A" and (row, column) == (2, 3) and diagram.dg[3][3] == "A" and diagram.dg[4][3] == "A" and diagram.dg[5][3] == "A") or
                        (char == "B" and (row, column) == (2, 5) and diagram.dg[3][5] == "B" and diagram.dg[4][5] == "B" and diagram.dg[5][5] == "B") or
                        (char == "C" and (row, column) == (2, 7) and diagram.dg[3][7] == "C" and diagram.dg[4][7] == "C" and diagram.dg[5][7] == "C") or
                            (char == "D" and (row, column) == (2, 9) and diagram.dg[3][9] == "D" and diagram.dg[4][9] == "D" and diagram.dg[5][9] == "D")):
                        continue

                cost = 1
                match char:
                    case 'B':
                        cost *= 10
                    case 'C':
                        cost *= 100
                    case 'D':
                        cost *= 1000

                # in and out of rooms
                room_map = {3: "A", 5: "B", 7: "C", 9: "D", }
                if diagram.dg[row+1][column-1] == '.' and room_map[column-1] == char and can_go_into_column(diagram, char):
                    new_diagram = diagram.get_copy()
                    new_diagram.dg[row+1][column -
                                          1] = new_diagram.dg[row][column]
                    new_diagram.dg[row][column] = '.'
                    new_diagram.cost += cost * 2
                    results.append(new_diagram)
                if diagram.dg[row+1][column+1] == '.' and room_map[column+1] == char and can_go_into_column(diagram, char):
                    new_diagram = diagram.get_copy()
                    new_diagram.dg[row+1][column +
                                          1] = new_diagram.dg[row][column]
                    new_diagram.dg[row][column] = '.'
                    new_diagram.cost += cost * 2
                    results.append(new_diagram)

                if diagram.dg[row-1][column-1] == '.':
                    new_diagram = diagram.get_copy()
                    new_diagram.dg[row-1][column -
                                          1] = new_diagram.dg[row][column]
                    new_diagram.dg[row][column] = '.'
                    new_diagram.cost += cost * 2
                    results.append(new_diagram)
                if diagram.dg[row-1][column+1] == '.':
                    new_diagram = diagram.get_copy()
                    new_diagram.dg[row-1][column +
                                          1] = new_diagram.dg[row][column]
                    new_diagram.dg[row][column] = '.'
                    new_diagram.cost += cost * 2
                    results.append(new_diagram)

                # inside the rooms
                if row > 2 and diagram.dg[row-1][column] == '.':
                    new_diagram = diagram.get_copy()
                    new_diagram.dg[row-1][column] = new_diagram.dg[row][column]
                    new_diagram.dg[row][column] = '.'
                    new_diagram.cost += cost
                    results.append(new_diagram)
                if diagram.dg[row+1][column] == '.':
                    new_diagram = diagram.get_copy()
                    new_diagram.dg[row+1][column] = new_diagram.dg[row][column]
                    new_diagram.dg[row][column] = '.'
                    new_diagram.cost += cost
                    results.append(new_diagram)

                # in the hallway
                if diagram.dg[row+1][column-1] != '#' and diagram.dg[row][column-2] == '.':
                    new_diagram = diagram.get_copy()
                    new_diagram.dg[row][column-2] = new_diagram.dg[row][column]
                    new_diagram.dg[row][column] = '.'
                    new_diagram.cost += cost * 2
                    results.append(new_diagram)
                if diagram.dg[row+1][column+1] != '#' and diagram.dg[row][column+2] == '.':
                    new_diagram = diagram.get_copy()
                    new_diagram.dg[row][column+2] = new_diagram.dg[row][column]
                    new_diagram.dg[row][column] = '.'
                    new_diagram.cost += cost * 2
                    results.append(new_diagram)

                # to the end of the hallway
                if diagram.dg[row+1][column-1] == '#' and diagram.dg[row][column-1] == '.':
                    new_diagram = diagram.get_copy()
                    new_diagram.dg[row][column-1] = new_diagram.dg[row][column]
                    new_diagram.dg[row][column] = '.'
                    new_diagram.cost += cost
                    results.append(new_diagram)
                if diagram.dg[row+1][column+1] == '#' and diagram.dg[row][column+1] == '.':
                    new_diagram = diagram.get_copy()
                    new_diagram.dg[row][column+1] = new_diagram.dg[row][column]
                    new_diagram.dg[row][column] = '.'
                    new_diagram.cost += cost
                    results.append(new_diagram)
    return results


def part1(input_list: list[str]) -> int:
    # return 0
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
            print("checked", count, "skipped", skip_count,
                  diagrams_to_check.qsize(), "in queue")
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
    input()
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
            print("checked", count, "skipped", skip_count,
                  diagrams_to_check.qsize(), "in queue")
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
