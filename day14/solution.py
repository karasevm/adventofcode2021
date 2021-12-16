import sys
from collections import Counter
from collections import defaultdict


def part1(input_list: list[str]) -> int:
    template = input_list[0]
    rules = {}
    for line in input_list[2:]:
        a, b = line.split(" -> ")
        rules[a] = b
    for _ in range(10):
        new_template = ""
        for i in range(1, len(template)):
            new_template += template[i-1]
            new_template += rules[template[i-1:i+1]]
        new_template += template[-1]
        template = new_template

    cntr = Counter(template)
    return cntr.most_common(1)[0][1] - cntr.most_common()[-1][1]


def part2(input_list: list[str]) -> int:
    template = input_list[0]
    rules = {}

    for line in input_list[2:]:
        a, b = line.split(" -> ")
        rules[a] = b

    pair_count = defaultdict(int)
    for i in range(1, len(template)):
        pair_count[template[i-1:i+1]] += 1

    letter_count = defaultdict(int)
    for letter, count in Counter(template).items():
        letter_count[letter] += count

    for _ in range(40):
        new_pair_count = defaultdict(int)

        for pair, occurrences in pair_count.items():
            letter_count[rules[pair]] += occurrences
            new_pair_count[f"{pair[0]}{rules[pair]}"] += occurrences
            new_pair_count[f"{rules[pair]}{pair[1]}"] += occurrences

        pair_count = new_pair_count

    return sorted(letter_count.values())[-1] - sorted(letter_count.values())[0]


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
