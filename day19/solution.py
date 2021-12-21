import sys
from typing import Deque
from copy import deepcopy
from collections import deque


class Beacon:
    def __init__(self,  x: int, y: int, z: int = 0):
        self.x = x
        self.y = y
        self.z = z
        self.neighbor_vectors = []

    def __eq__(self, other):
        if isinstance(other, Beacon):
            return (self.x == other.x and
                    self.y == other.y and
                    self.z == other.z)
        return False

    def __lt__(self, other):
        return self.x < other.x

    def __repr__(self):
        return f"[{self.x}, {self.y}, {self.z}]"

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __deepcopy__(self, memodict={}):
        copy_object = Beacon(self.x, self.y, self.z)
        for neighbor in self.neighbor_vectors:
            copy_object.add_neighbor(*neighbor)
        return copy_object

    def add_neighbor(self, x: int, y: int, z: int = 0):
        self.neighbor_vectors.append((x, y, z))

    def get_rotated(self, facing: int, rotation: int) -> 'Beacon':
        beacon_copy = deepcopy(self)
        for i in range(rotation):  # rotate around the z axis
            beacon_copy.x, beacon_copy.y = beacon_copy.y, -beacon_copy.x
            for index, vector in enumerate(beacon_copy.neighbor_vectors):
                x, y, z = vector
                beacon_copy.neighbor_vectors[index] = (y, -x, z)

        if facing < 4:  # four directions around the y axis
            for i in range(facing):
                beacon_copy.x, beacon_copy.z = -beacon_copy.z, beacon_copy.x
                for index, vector in enumerate(beacon_copy.neighbor_vectors):
                    x, y, z = vector
                    beacon_copy.neighbor_vectors[index] = (-z, y, x)
        elif facing == 4:  # facing toward positive y
            beacon_copy.y, beacon_copy.z = -beacon_copy.z, beacon_copy.y
            for index, vector in enumerate(beacon_copy.neighbor_vectors):
                x, y, z = vector
                beacon_copy.neighbor_vectors[index] = (x, -z, y)
        elif facing == 5:  # facing toward negative y
            beacon_copy.y, beacon_copy.z = beacon_copy.z, -beacon_copy.y
            for index, vector in enumerate(beacon_copy.neighbor_vectors):
                x, y, z = vector
                beacon_copy.neighbor_vectors[index] = (x, z, -y)
        return beacon_copy


class Scanner:
    def __init__(self, id: int):
        self.beacons: list[Beacon] = []
        self.x = 0
        self.y = 0
        self.z = 0
        self.id = id

    def add_beacon(self, beacon: Beacon):
        self.beacons.append(beacon)

    def __str__(self):
        output = f"Scanner {self.id}\n"
        for beacon in self.beacons:
            output += f"{beacon.x}, {beacon.y}, {beacon.z}\n"
        return output

    def __repr__(self):
        output = f"<Scanner id:{self.id} "
        for beacon in self.beacons[:-1]:
            output += f"[{beacon.x}, {beacon.y}, {beacon.z}], "
        output += f"[{self.beacons[-1].x}, {self.beacons[-1].y}, {self.beacons[-1].z}]>"
        return output

    def __eq__(self, other):
        if isinstance(other, Scanner):
            return (self.id == other.id)
        return False

    def get_rotated(self, facing: int, rotation: int) -> 'Scanner':
        scanner_copy = deepcopy(self)
        for i in range(len(scanner_copy.beacons)):
            scanner_copy.beacons[i] = self.beacons[i].get_rotated(
                facing, rotation)

        return scanner_copy

    def get_offset(self, x: int, y: int, z: int) -> 'Scanner':
        scanner_copy = deepcopy(self)
        scanner_copy.x = x
        scanner_copy.y = y
        scanner_copy.z = z
        for i in range(len(self.beacons)):
            scanner_copy.beacons[i].x += x
            scanner_copy.beacons[i].y += y
            scanner_copy.beacons[i].z += z

        return scanner_copy


def parse_scanners(input_list: list[str]) -> list[Scanner]:
    scanners: list[Scanner] = []
    current_scanner = Scanner(0)
    for line in input_list:
        if line[:12] == "--- scanner ":
            current_scanner = Scanner(int(line[12:14]))
        elif len(line) == 0:
            scanners.append(current_scanner)
        else:
            try:
                x, y, z = [int(x) for x in line.split(',')]
                current_scanner.add_beacon(Beacon(x, y, z))
            except:
                x, y = [int(x) for x in line.split(',')]
                current_scanner.add_beacon(Beacon(x, y))

    scanners.append(current_scanner)
    for scanner in scanners:
        for beacon in scanner.beacons:
            for other_beacon in scanner.beacons:
                if beacon != other_beacon:
                    x = other_beacon.x - beacon.x
                    y = other_beacon.y - beacon.y
                    z = other_beacon.z - beacon.z
                    beacon.add_neighbor(x, y, z)
    return scanners


def count_overlap_for_scanners(scanner_a: Scanner, scanner_b: Scanner) -> tuple[int, list[Beacon], tuple[int, int, int, int, int]]:
    beacons = []
    scanner_b_orientation: tuple[int, int, int, int, int] = (0, 0, 0, 0, 0)
    for facing in range(6):
        for rotation in range(4):
            for beacon_a in scanner_a.beacons:
                for beacon_b in scanner_b.beacons:
                    rotated_beacon_b = beacon_b.get_rotated(facing, rotation)
                    overlap = len(set(beacon_a.neighbor_vectors)
                                  & set(rotated_beacon_b.neighbor_vectors))
                    if overlap >= 2:  # if beacon_a has at least the same 2 neighbors as rotated beacon b
                        scanner_b_orientation = (beacon_a.x-rotated_beacon_b.x,
                                                 beacon_a.y-rotated_beacon_b.y,
                                                 beacon_a.z-rotated_beacon_b.z,
                                                 facing,
                                                 rotation)
                        beacons.append(beacon_a)
                        break
            if len(beacons) != 0:
                return len(beacons), beacons, scanner_b_orientation
    return len(beacons), beacons, scanner_b_orientation


def solve(scanners: list[Scanner]) -> tuple[int, int]:
    scanner_a_queue: Deque[Scanner] = deque()
    scanner_a_queue.append(scanners[0])
    visited = set()
    while scanner_a_queue:
        a = scanner_a_queue.popleft()
        if a.id in visited:
            continue
        visited.add(a.id)
        for b in range(len(scanners)):
            if a != scanners[b]:
                count, beacons, (x, y, z, facing, rotation) = count_overlap_for_scanners(
                    a, scanners[b])
                if count >= 12:
                    scanners[b] = scanners[b].get_rotated(
                        facing, rotation).get_offset(x, y, z)
                    scanner_a_queue.append(scanners[b])
                # print(f"Scanners {a.id} and {scanners[b].id}({x}, {y}, {z}, {facing}, {rotation}) have {count} overlapping beacons at {beacons}")
    beacons = set()
    for scanner in scanners:
        # print(f"Scanner {scanner.id} is at {scanner.x}, {scanner.y}, {scanner.z} has beacons {sorted(scanner.beacons)}\n")
        beacons.update(scanner.beacons)
    # print(sorted(list(beacons)))

    max_distance = 0
    for scanner_a in scanners:
        for scanner_b in scanners:
            distance = abs(scanner_a.x - scanner_b.x) + abs(scanner_a.y -
                                                            scanner_b.y) + abs(scanner_a.z - scanner_b.z)
            if distance > max_distance:
                # print(scanner_a, scanner_b)
                max_distance = distance
    # print("max dist", max_distance)

    return len(beacons), max_distance


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
        scanners = parse_scanners(lines)
        part1, part2 = solve(scanners)
        print(
            f"Part 1 answer: {part1} Part 2 answer: {part2}")
