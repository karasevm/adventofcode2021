import sys


def part1(input_list: list[str]) -> int:
    numbers = [int(item) for item in input_list[0].split(',')]
    for _ in range(80):
        for i in range(len(numbers)):
            if numbers[i] == 0:
                numbers.append(8)
                numbers[i] = 6
            else:
                numbers[i] -= 1
    return len(numbers)


def part2(input_list: list[str]) -> int:
    numbers = [int(item) for item in input_list[0].split(',')]
    fish_counts = [0] * 7
    growing_fish_counts = [0] * 2
    for number in numbers:
        fish_counts[number] += 1
    for _ in range(256):
        new_fish = fish_counts.pop(0)
        growing_fish_counts.append(new_fish)
        fish_counts.append(new_fish + growing_fish_counts.pop(0))
    return sum(fish_counts) + sum(growing_fish_counts)


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
