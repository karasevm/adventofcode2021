use std::fs::File;
use std::io::{BufRead, BufReader};
use std::{cmp, env, vec};

fn part1(input: &Vec<String>) -> i32 {
    let mut numbers: Vec<i32> = input[0]
        .split(',')
        .map(|x| x.parse::<i32>().unwrap())
        .collect();
    numbers.sort();
    let median = numbers[numbers.len() / 2];
    let mut fuel = 0;
    for number in numbers {
        fuel += (number - median).abs()
    }
    fuel
}

fn part2(input: &Vec<String>) -> i32 {
    let numbers: Vec<i32> = input[0]
        .split(',')
        .map(|x| x.parse::<i32>().unwrap())
        .collect();
    let average = numbers.iter().sum::<i32>() as f32 / numbers.len() as f32;
    let averages = vec![average.floor() as i32, average.ceil() as i32];
    let mut fuels = vec![0, 0];
    for (i, a) in averages.iter().enumerate() {
        for number in &numbers {
            let diff = (number - a).abs();
            fuels[i] += (diff * (diff + 1)) / 2;
        }
    }
    cmp::min(fuels[0], fuels[1])
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
