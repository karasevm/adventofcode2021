import sys
from collections import deque



def part1(input_list: list[str]) -> int:
    numbers = [[int(number) for number in line] for line in input_list]
    octopuses_to_flash = deque()
    count = 0
    for _ in range(100):
        for line in range(len(numbers)):
            for number in range(len(numbers)):
                if numbers[line][number] == 9:
                    octopuses_to_flash.append((line,number))
                numbers[line][number] += 1
                    
        while octopuses_to_flash:
            line, number = octopuses_to_flash.popleft()
            numbers[line][number] = 0
            count += 1
            coords_to_check = []
            if line != 0:
                coords_to_check.append((line-1, number))
                if number != 0:
                    coords_to_check.append((line-1, number-1))
                if number != len(numbers[0])-1:
                    coords_to_check.append((line-1, number+1))
            if number != 0:
                coords_to_check.append((line, number-1))
            if number != len(numbers[0])-1:
                coords_to_check.append((line, number+1))
            if line != len(numbers)-1:
                coords_to_check.append((line+1, number))
                if number != 0:
                    coords_to_check.append((line+1, number-1))
                if number != len(numbers[0])-1:
                    coords_to_check.append((line+1, number+1))
            for line, number in coords_to_check:
                
                if numbers[line][number] == 0:
                    continue
                if numbers[line][number] == 9:
                    octopuses_to_flash.append((line,number))
                numbers[line][number] += 1


    return count


def part2(input_list: list[str]) -> int:
    numbers = [[int(number) for number in line] for line in input_list]
    octopuses_to_flash = deque()
    count = 0
    while True:
        count += 1
        if sum([sum(line) for line in numbers]) == 0:
            return count - 1
        for line in range(len(numbers)):
            for number in range(len(numbers)):
                if numbers[line][number] == 9:
                    octopuses_to_flash.append((line,number))
                numbers[line][number] += 1
                    
        while octopuses_to_flash:
            line, number = octopuses_to_flash.popleft()
            numbers[line][number] = 0
            coords_to_check = []
            
            if line != 0:
                coords_to_check.append((line-1, number))
                if number != 0:
                    coords_to_check.append((line-1, number-1))
                if number != len(numbers[0])-1:
                    coords_to_check.append((line-1, number+1))
            if number != 0:
                coords_to_check.append((line, number-1))
            if number != len(numbers[0])-1:
                coords_to_check.append((line, number+1))
            if line != len(numbers)-1:
                coords_to_check.append((line+1, number))
                if number != 0:
                    coords_to_check.append((line+1, number-1))
                if number != len(numbers[0])-1:
                    coords_to_check.append((line+1, number+1))

            for line, number in coords_to_check:
                if numbers[line][number] == 0:
                    continue
                if numbers[line][number] == 9:
                    octopuses_to_flash.append((line,number))
                numbers[line][number] += 1


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
