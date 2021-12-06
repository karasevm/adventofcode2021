use std::collections::VecDeque;
use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn solve(input: &Vec<i32>, iterations: i32) -> i64 {
    let mut fish_counts = VecDeque::from([0; 7]);
    let mut growing_fish_counts = VecDeque::from([0; 2]);
    for number in input {
        fish_counts[*number as usize] += 1;
    }
    for _ in 0..iterations {
        let new_fish = fish_counts.pop_front().unwrap();
        growing_fish_counts.push_back(new_fish);
        fish_counts.push_back(new_fish + growing_fish_counts.pop_front().unwrap())
    }
    return fish_counts.iter().sum::<i64>() + growing_fish_counts.iter().sum::<i64>();
}

fn part1(input: &Vec<String>) -> i64 {
    let numbers: Vec<i32> = input[0]
        .split(',')
        .map(|x| x.parse::<i32>().unwrap())
        .collect();
    solve(&numbers, 80)
}

fn part2(input: &Vec<String>) -> i64 {
    let numbers: Vec<i32> = input[0]
        .split(',')
        .map(|x| x.parse::<i32>().unwrap())
        .collect();
    solve(&numbers, 256)
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
