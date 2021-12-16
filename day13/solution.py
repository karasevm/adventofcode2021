import sys
from collections import deque

MATRIX_SIZE = 1500
def part1(input_list: list[str]) -> int:
    matrix = [['.' for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]
    fold_directions = []
    for index, line in enumerate(input_list):
        if len(line) == 0:
            fold_directions = input_list[index+1:]
            break
        x = int(line.split(',')[0])
        y = int(line.split(',')[1])
        matrix[y][x] = "#"
    
    if fold_directions[0][11] == 'y':
        new_matrix = [['.' for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]
        fold_at = int(fold_directions[0][13:])

        # copy upper part
        for y in range(fold_at):
            for x in range(MATRIX_SIZE):
                new_matrix[y][x] = matrix[y][x]
        # copy lower part
        for y in range(fold_at + 1, fold_at * 2 + 1):
            for x in range(MATRIX_SIZE):
                print(f"Setting {fold_at - (y - fold_at)} {x} to {y} {x}")
                if matrix[y][x] == '#':
                    new_matrix[fold_at - (y - fold_at)][x] = matrix[y][x]
        
        matrix = new_matrix
    else:
        new_matrix = [['.' for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]
        fold_at = int(fold_directions[0][13:])

        # copy left part
        for y in range(MATRIX_SIZE):
            for x in range(fold_at):
                new_matrix[y][x] = matrix[y][x]
        # copy right part
        for y in range(MATRIX_SIZE):
            for x in range(fold_at + 1, fold_at * 2 + 1):
                # print(f"Setting {fold_at - (x - fold_at)} {y} to {x} {y}")
                if matrix[y][x] == '#':
                    new_matrix[y][fold_at - (x - fold_at)] = matrix[y][x]
        
        matrix = new_matrix
        
    result = 0
    for line in matrix:
        result += line.count('#')
    return result


def part2(input_list: list[str]) -> int:
    matrix = [['.' for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]
    fold_directions = []
    for index, line in enumerate(input_list):
        if len(line) == 0:
            fold_directions = input_list[index+1:]
            break
        x = int(line.split(',')[0])
        y = int(line.split(',')[1])
        matrix[y][x] = "#"
    for fold in fold_directions:
        if fold[11] == 'y':
            new_matrix = [['.' for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]
            fold_at = int(fold[13:])

            # copy upper part
            for y in range(fold_at):
                for x in range(MATRIX_SIZE):
                    new_matrix[y][x] = matrix[y][x]
            # copy lower part
            for y in range(fold_at + 1, fold_at * 2 + 1):
                for x in range(MATRIX_SIZE):
                    if matrix[y][x] == '#':
                        new_matrix[fold_at - (y - fold_at)][x] = matrix[y][x]
            
            matrix = new_matrix
        else:
            new_matrix = [['.' for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]
            fold_at = int(fold[13:])

            # copy left part
            for y in range(MATRIX_SIZE):
                for x in range(fold_at):
                    new_matrix[y][x] = matrix[y][x]
            # copy right part
            for y in range(MATRIX_SIZE):
                for x in range(fold_at + 1, fold_at * 2 + 1):
                    # print(f"Setting {fold_at - (x - fold_at)} {y} to {x} {y}")
                    if matrix[y][x] == '#':
                        new_matrix[y][fold_at - (x - fold_at)] = matrix[y][x]
            
            matrix = new_matrix
        
    print("Part 2 answer:")
    for line in matrix:
        if line.count("#") > 0:
            print(''.join(line[:40]))
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
