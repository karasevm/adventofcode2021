import sys
from collections import deque
from functools import reduce

def part1(input_list: list[str]) -> int:
    height_matrix = [[int(number) for number in line] for line in input_list]
    result = 0
    for line_index, line in enumerate(height_matrix):
        for number_index, number in enumerate(line):
            if ((line_index == 0 or height_matrix[line_index-1][number_index] > number) and
                (number_index == 0 or height_matrix[line_index][number_index-1] > number) and
                (number_index == len(line)-1 or height_matrix[line_index][number_index+1] > number) and
                (line_index == len(height_matrix)-1 or height_matrix[line_index+1][number_index] > number)):
                result += number + 1
    return result

def find_basin_size(matrix: list[list[int]], line: int, number: int) -> int:
    coords_to_check = deque([(line,number)])
    matrix_height = len(matrix)
    matrix_width = len(matrix[0])
    coords_list = []
    while coords_to_check:
        iter_line, iter_number = coords_to_check.pop()
        current_number = matrix[iter_line][iter_number]
        if current_number == 9:
            continue
        if iter_line > 0 and matrix[iter_line-1][iter_number] > current_number:
            coords_to_check.append((iter_line-1, iter_number))
        if iter_line < matrix_height - 1 and matrix[iter_line+1][iter_number] > current_number:
            coords_to_check.append((iter_line+1, iter_number))
        if iter_number > 0 and matrix[iter_line][iter_number-1] > current_number:
            coords_to_check.append((iter_line, iter_number-1))
        if iter_number < matrix_width - 1 and matrix[iter_line][iter_number+1] > current_number:
            coords_to_check.append((iter_line, iter_number+1))
        coords_list.append((iter_line, iter_number))
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if (i,j) in coords_list:
                print(f"\u001b[31m{matrix[i][j]}\u001b[0m", end="")
            else:
                print(f"{matrix[i][j]}", end="")
        print("\n", end="")
            
    return len(set(coords_list))

def part2(input_list: list[str]) -> int:
    height_matrix = [[int(number) for number in line] for line in input_list]
    basin_sizes = []
    for line_index, line in enumerate(height_matrix):
        for number_index, number in enumerate(line):
            if ((line_index == 0 or height_matrix[line_index-1][number_index] > number) and
                (number_index == 0 or height_matrix[line_index][number_index-1] > number) and
                (number_index == len(line)-1 or height_matrix[line_index][number_index+1] > number) and
                (line_index == len(height_matrix)-1 or height_matrix[line_index+1][number_index] > number)):
                basin_sizes.append(find_basin_size(height_matrix, line_index, number_index))
    return reduce(lambda x,y: x*y,sorted(basin_sizes)[-3:])


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
