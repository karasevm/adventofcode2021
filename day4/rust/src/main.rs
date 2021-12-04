use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn parse_boards(input: &Vec<String>) -> Vec<Vec<Vec<i32>>> {
    let mut boards: Vec<Vec<Vec<i32>>> = Vec::new();
    for i in (1..input.len()).step_by(6) {
        let mut tmp_board: Vec<Vec<i32>> = Vec::new();
        for j in 0..5 {
            tmp_board.push(
                input[i + j + 1]
                    .split_whitespace()
                    .map(|x| x.parse().unwrap())
                    .collect(),
            )
        }
        boards.push(tmp_board)
    }
    boards
}

fn list_consists_of_elements(list: &Vec<i32>, elements: &Vec<i32>) -> bool {
    for element in list {
        if !elements.contains(&element) {
            return false;
        }
    }
    true
}

fn check_board(board: &Vec<Vec<i32>>, numbers: &Vec<i32>) -> bool {
    for line in board {
        if list_consists_of_elements(&line, numbers) {
            return true;
        }
    }
    for i in 0..board[0].len() {
        let mut tmp_vec: Vec<i32> = Vec::new();
        for j in 0..board.len() {
            tmp_vec.push(board[j][i])
        }
        if list_consists_of_elements(&tmp_vec, numbers) {
            return true;
        }
    }
    false
}

fn calculate_board_score(board: &Vec<Vec<i32>>, numbers: &Vec<i32>) -> i32 {
    let mut new_board: Vec<Vec<i32>> = Vec::new();
    for line in board {
        new_board.push(
            line.iter()
                .filter(|x| !numbers.contains(x))
                .cloned()
                .collect(),
        )
    }
    new_board.iter().map(|x| x.iter().sum::<i32>()).sum::<i32>() * numbers.last().clone().unwrap()
}

fn part1(input: &Vec<String>) -> i32 {
    let numbers: Vec<i32> = input[0]
        .split(',')
        .map(|x| x.parse::<i32>().unwrap())
        .collect();
    let boards = parse_boards(input);
    let mut draws_to_win = vec![std::i32::MAX; boards.len()];

    for i in 0..numbers.len() {
        for j in 0..boards.len() {
            if draws_to_win[j] == std::i32::MAX && check_board(&boards[j], &numbers[0..i].to_vec())
            {
                draws_to_win[j] = i as i32
            }
        }
    }

    let mut min_board = std::i32::MAX;
    let mut min_board_index = 0;
    for (i, draws) in draws_to_win.iter().enumerate() {
        if draws < &min_board {
            min_board = *draws;
            min_board_index = i;
        }
    }
    calculate_board_score(
        &boards[min_board_index],
        &numbers[..(min_board as usize)].to_vec(),
    )
}

fn part2(input: &Vec<String>) -> i32 {
    let numbers: Vec<i32> = input[0]
        .split(',')
        .map(|x| x.parse::<i32>().unwrap())
        .collect();
    let boards = parse_boards(input);
    let mut draws_to_win = vec![std::i32::MAX; boards.len()];

    for i in 0..numbers.len() {
        for j in 0..boards.len() {
            if draws_to_win[j] == std::i32::MAX && check_board(&boards[j], &numbers[0..i].to_vec())
            {
                draws_to_win[j] = i as i32
            }
        }
    }

    let mut max_board = std::i32::MIN;
    let mut max_board_index = 0;
    for (i, draws) in draws_to_win.iter().enumerate() {
        if draws > &max_board {
            max_board = *draws;
            max_board_index = i;
        }
    }
    calculate_board_score(
        &boards[max_board_index],
        &numbers[..(max_board as usize)].to_vec(),
    )
}

fn main() {
    let filename = env::args().nth(1).expect("Missing argument");
    let file = File::open(filename).expect("No such file");
    let buf = BufReader::new(file);
    let lines = buf.lines();

    let contents = lines.map(|l| l.expect("Could not parse line")).collect();
    println!(
        "Part 1 answer:{} Part 2 answer:{}",
        part1(&contents),
        part2(&contents)
    );
}
