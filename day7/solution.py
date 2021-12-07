import sys
import math

def part1(input_list: list[str]) -> int:
    numbers = [int(item) for item in input_list[0].split(',')]
    numbers.sort()
    median = numbers[len(numbers)//2]
    fuel = 0
    for number in numbers:
        fuel += abs(number - median)
    return fuel


def part2(input_list: list[str]) -> int:
    numbers = [int(item) for item in input_list[0].split(',')]
    average = sum(numbers) / len(numbers)
    averages = [math.ceil(average), math.floor(average)]
    print(averages)
    fuels = [0, 0]
    for i, a in enumerate(averages):
        for number in numbers:
            fuels[i] += sum(range(abs(number - a) + 1))
    return min(*fuels)


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
