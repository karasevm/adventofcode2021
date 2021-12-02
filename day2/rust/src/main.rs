use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn part1(input: &Vec<String>) -> i32 {
    let mut pos_x = 0;
    let mut pos_y = 0;
    for input_command in input.iter() {
        let inputs = input_command.split(" ").collect::<Vec<&str>>();
        match inputs[0] {
            "forward" => pos_x += inputs[1].parse::<i32>().unwrap(),
            "down" => pos_y += inputs[1].parse::<i32>().unwrap(),
            "up" => pos_y -= inputs[1].parse::<i32>().unwrap(),
            _ => (),
        }
    }
    pos_x * pos_y
}

fn part2(input: &Vec<String>) -> i32 {
    let mut pos_x = 0;
    let mut pos_y = 0;
    let mut aim = 0;
    for input_command in input.iter() {
        let inputs = input_command.split(" ").collect::<Vec<&str>>();
        match inputs[0] {
            "forward" => {
                pos_x += inputs[1].parse::<i32>().unwrap();
                pos_y += aim * inputs[1].parse::<i32>().unwrap();
            }
            "down" => aim += inputs[1].parse::<i32>().unwrap(),
            "up" => aim -= inputs[1].parse::<i32>().unwrap(),
            _ => (),
        }
    }
    pos_x * pos_y
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
