from functools import cache
import sys
import operator


def get_die_roll():
    first_die = 0
    while True:
        yield ((first_die % 100) + 1, (first_die % 100) + 2, (first_die % 100) + 3)
        first_die += 3


def part1(input_list: list[str]) -> int:
    player_scores = [0, 0]
    player_positions = [int(input_list[0][-1]) - 1, int(input_list[1][-1]) - 1]

    player_1_turn = True
    roll_count = 0
    for die_sum in get_die_roll():
        roll_count += 3
        print(
            f"Player {'1' if player_1_turn else '2'} rolls {die_sum} ", end="")
        if player_1_turn:
            player_positions[0] = (player_positions[0] + sum(die_sum)) % 10
            player_scores[0] += player_positions[0] + 1
            print(
                f"and moves to space {player_positions[0] + 1} for a total score of {player_scores[0]}")
            if player_scores[0] >= 1000:
                print(player_scores[1], roll_count)
                return player_scores[1] * roll_count
        else:
            player_positions[1] = (player_positions[1] + sum(die_sum)) % 10
            player_scores[1] += player_positions[1] + 1
            print(
                f"and moves to space {player_positions[1] + 1} for a total score of {player_scores[1]}")
            if player_scores[1] >= 1000:
                print(player_scores[0], roll_count)
                return player_scores[0] * roll_count
        player_1_turn = not player_1_turn
    return 0


@cache
def dirac_die_game(player_positions: tuple[int, int], player_scores: tuple[int, int], player_1_turn: bool):
    player_win_count = (0, 0)
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                if player_1_turn:
                    player_1_pos = (player_positions[0] + sum([i, j, k])) % 10
                    player_1_score = player_scores[0] + player_1_pos + 1
                    if player_1_score >= 21:
                        player_win_count = tuple(
                            map(operator.add, player_win_count, (1, 0)))
                    else:
                        player_win_count = tuple(map(operator.add,
                                                     player_win_count,
                                                     dirac_die_game((player_1_pos, player_positions[1]),
                                                                    (player_1_score,
                                                                     player_scores[1]),
                                                                    not player_1_turn)))
                else:
                    player_2_pos = (player_positions[1] + sum([i, j, k])) % 10
                    player_2_score = player_scores[1] + player_2_pos + 1
                    if player_2_score >= 21:
                        player_win_count = tuple(
                            map(operator.add, player_win_count, (0, 1)))
                    else:
                        player_win_count = tuple(map(operator.add,
                                                     player_win_count,
                                                     dirac_die_game((player_positions[0], player_2_pos),
                                                                    (player_scores[0],
                                                                     player_2_score),
                                                                    not player_1_turn)))
    return player_win_count


def part2(input_list: list[str]) -> int:

    player_scores = [0, 0]
    player_positions = [int(input_list[0][-1]) - 1, int(input_list[1][-1]) - 1]

    result = dirac_die_game(tuple(player_positions),
                            tuple(player_scores), True)
    return max(result)


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
