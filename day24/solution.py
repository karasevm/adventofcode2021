
from collections import deque
import sys
from functools import cache

@cache
def proccess_input(ops: tuple[list[str]], input_values: tuple[int], z: int = 0) -> dict[str,int]:
    registers = {"w": 0, "x": 0, "y": 0, "z": z}
    input_queue = deque()
    input_queue.extend(input_values)
    for op in ops:
        second_arg = 0
        if op[0] != 'inp':
            try:
                second_arg = registers[op[2]]
            except Exception as e:
                second_arg = int(op[2])
        match op[0]:
            case 'inp':
                registers[op[1]] = input_queue.popleft()
            case 'add':
                registers[op[1]] = registers[op[1]] + second_arg 
            case 'mul':
                registers[op[1]] = registers[op[1]] * second_arg 
            case 'div':
                registers[op[1]] = registers[op[1]] // second_arg 
            case 'mod':
                registers[op[1]] = registers[op[1]] % second_arg 
            case 'eql':
                registers[op[1]] = 1 if registers[op[1]] == second_arg else 0

    return registers

def part1(input_list: list[str]) -> int:
    ops = [tuple(line.split(" ")) for line in input_list]

    ops_part = []
    tmp = []

    for op in ops:
        if op[0] == 'inp':
            ops_part.append(tuple(tmp))
            tmp = []
        tmp.append(op)
    
    ops_part = ops_part[1:]
    ops_part.append(tuple(tmp))
    registers = {"w": 0, "x": 0, "y": 0, "z": 0}
    z = {0:0}
    for part in ops_part:
        new_z = {}
        for serial in range(9, 0,-1):
            for cz,path in z.items():
                registers = {"w": 0, "x": 0, "y": 0, "z": cz}
                registers = proccess_input(part, (serial,), cz)
                new_path = path*10+serial
                # Store only the biggest inputs for resulting outputs, truncate outputs to be less that 10000000
                if registers["z"] < 10000000 and (registers["z"] not in new_z.keys() or new_path > new_z[registers["z"]]):
                    new_z[registers["z"]]=new_path
        z = new_z
    
    return z[0]


def part2(input_list: list[str]) -> int:
    ops = [tuple(line.split(" ")) for line in input_list]

    ops_part = []
    tmp = []

    for op in ops:
        if op[0] == 'inp':
            ops_part.append(tuple(tmp))
            tmp = []
        tmp.append(op)
    
    ops_part = ops_part[1:]
    ops_part.append(tuple(tmp))
    registers = {"w": 0, "x": 0, "y": 0, "z": 0}
    z = {0:0}
    for part in ops_part:
        new_z = {}
        for serial in range(9, 0,-1):
            for cz,path in z.items():
                registers = {"w": 0, "x": 0, "y": 0, "z": cz}
                registers = proccess_input(part, (serial,), cz)
                new_path = path*10+serial
                # Store only the biggest input for each output, truncate outputs to be less that 10000000
                if registers["z"] < 10000000 and (registers["z"] not in new_z.keys() or new_path < new_z[registers["z"]]):
                    new_z[registers["z"]]=new_path
        z = new_z
    
    return z[0]


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
