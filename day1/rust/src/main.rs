use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn part1(input: &Vec<i32>) -> i32 {
    let mut output = 0;
    for i in 1..input.len() {
        if input[i] > input[i - 1] {
            output += 1
        }
    }
    output
}

fn part2(input: &Vec<i32>) -> i32 {
    let mut output = 0;
    for i in 4..input.len() + 1 {
        if input[i - 3..i].iter().sum::<i32>() > input[i - 4..i - 1].iter().sum::<i32>() {
            output += 1
        }
    }
    output
}

fn main() {
    let filename = env::args().nth(1).expect("Missing argument");
    let file = File::open(filename).expect("No such file");
    let buf = BufReader::new(file);
    let lines = buf.lines();

    let contents: Vec<i32> = lines.map(|x| x.unwrap().parse::<i32>().unwrap()).collect();

    println!(
        "Part 1 answer:{} Part 2 answer:{}",
        part1(&contents),
        part2(&contents)
    );
}
