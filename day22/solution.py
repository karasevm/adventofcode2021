
import sys
from collections import defaultdict, deque
import re

def part1(input_list: list[str]) -> int:
    input_regex = re.compile(r"^(\w+)\sx=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)$")
    grid: defaultdict[tuple[int,int,int], bool] = defaultdict(bool)
    for line in input_list:
        matches = input_regex.search(line)
        assert matches
        state = True if matches.group(1) == 'on' else False

        x = (int(matches.group(2)),int(matches.group(3)))
        y = (int(matches.group(4)),int(matches.group(5)))
        z = (int(matches.group(6)),int(matches.group(7)))
        
        
        for x in range(max(-50,int(matches.group(2))),min(50,int(matches.group(3)))+1):
            for y in range(max(-50,int(matches.group(4))),min(50,int(matches.group(5)))+1):
               for z in range(max(-50,int(matches.group(6))),min(50,int(matches.group(7)))+1):
                   grid[(x,y,z)] = state
        
    count = 0
    for _,v in grid.items():
        if v:
            count+= 1
    
    return count

class Cuboid:
    def __init__(self, start: tuple[int,int,int], end: tuple[int,int,int]):
        self.ax = start[0]
        self.ay = start[1]
        self.az = start[2]
        self.bx = end[0]
        self.by = end[1]
        self.bz = end[2]

    def __eq__(self, other):
        return self.ax == other.ax and self.ay == other.ay and self.az == other.az and self.bx == other.bx and self.by == other.by and self.bz == other.bz 
    
    def get_volume(self) -> int:
        return (self.bx + 1 - self.ax) * (self.by + 1 - self.ay) * (self.bz + 1 - self.az)

    def __hash__(self) -> int:
        return hash((self.bx,self.ax,self.by ,self.ay,self.bz,self.az))
    
    def __repr__(self):
        return f"<Cuboid x={self.ax}..{self.bx} y={self.ay}..{self.by} z={self.az}..{self.bz}>"

def apply_negative(positive_list: list[Cuboid], negative: Cuboid) -> list[Cuboid]:
    """Given a list of cuboids and a single cuboid produce such a list of 
    cuboids that cover the same space, except for the provided single cuboid is 
    replaced with empty space

    Args:
        positive_list (list[Cuboid]): List of cuboids to substract from
        negative (Cuboid): Cuboid to substract

    Returns:
        list[Cuboid]: List of cuboids with empty space
    """
    results: list[Cuboid] = []
    for shape in positive_list:
        x = (max(shape.ax, negative.ax),min(shape.bx, negative.bx))
        y = (max(shape.ay, negative.ay),min(shape.by, negative.by))
        z = (max(shape.az, negative.az),min(shape.bz, negative.bz))
        if x[1] < x[0] or y[1] < y[0] or z[1] < z[0]: # no overlap
            results.append(shape)
        else:
            # block to the left
            results.append(Cuboid((shape.ax,shape.ay,shape.az), (x[0]-1, shape.by, shape.bz)))
            # block to the right
            results.append(Cuboid((x[1]+1,shape.ay,shape.az), (shape.bx, shape.by, shape.bz)))
            # block to the bottom
            results.append(Cuboid((x[0],shape.ay,shape.az), (x[1], y[0] - 1, shape.bz)))
            # block to the top
            results.append(Cuboid((x[0],y[1] + 1,shape.az), (x[1],shape.by , shape.bz)))
            # block in front
            results.append(Cuboid((x[0],y[0],shape.az), (x[1], y[1], z[0] - 1)))
            # block behind
            results.append(Cuboid((x[0],y[0],z[1] + 1), (x[1], y[1], shape.bz)))

    return [result for result in results if (result.ax <= result.bx and result.ay <= result.by and result.az <= result.bz) ]

def find_non_overlapping_volume(cuboids: list[Cuboid]) -> int:
    results = []
    cuboid_queue: deque[Cuboid] = deque()
    cuboid_queue.extend(cuboids)

    # Substract each cuboid from the remaining and add it to the list
    while cuboid_queue:
        current_cuboid = cuboid_queue.popleft()
        tmp_queue = deque()
        tmp_queue.extend(apply_negative(list(cuboid_queue), current_cuboid))
        cuboid_queue = tmp_queue
        results.append(current_cuboid)
    return sum([x.get_volume() for x in results])
                
def part2(input_list: list[str]) -> int:
    input_regex = re.compile(r"^(\w+)\sx=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)$")
    positive: list[Cuboid] = []
    for line in input_list:

        matches = input_regex.search(line)
        assert matches
        state = True if matches.group(1) == 'on' else False
        x = (int(matches.group(2)),int(matches.group(3)))
        y = (int(matches.group(4)),int(matches.group(5)))
        z = (int(matches.group(6)),int(matches.group(7)))
        
        if state:
            positive.append(Cuboid((int(matches.group(2)),int(matches.group(4)),int(matches.group(6))),
                                    (int(matches.group(3)),int(matches.group(5)),int(matches.group(7)))))
        else:
            positive = apply_negative(positive, Cuboid((x[0],y[0],z[0]),(x[1],y[1],z[1])))
    
    return find_non_overlapping_volume(positive)


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
