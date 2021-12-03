use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn count_ones_in_column(input: &Vec<String>, column: usize) -> usize {
    let mut total = 0;
    for row in input {
        if row.as_bytes()[column] as char == '1' {
            total += 1;
        }
    }
    total
}

fn make_mask(bit_count: usize) -> u32 {
    let mut mask: u32 = 0;
    for _ in 0..bit_count {
        mask = mask << 1;
        mask = mask | 1;
    }
    mask
}

fn part1(input: &Vec<String>) -> u32 {
    let mut result_gamma: u32 = 0;

    for column in 0..input[0].len() {
        result_gamma = result_gamma << 1;
        if count_ones_in_column(input, column) > input.len() / 2 {
            result_gamma = result_gamma | 1
        }
    }

    result_gamma * (!result_gamma & make_mask(input[0].len()))
}

fn part2(input: &Vec<String>) -> u32 {
    let mut modified_input = input.to_vec();
    for i in 0..modified_input.len() {
        if modified_input.len() == 1 {
            break;
        }
        if count_ones_in_column(&modified_input, i) * 2 >= modified_input.len() {
            modified_input = modified_input
                .into_iter()
                .filter(|x| x.as_bytes()[i] as char == '1')
                .collect();
        } else {
            modified_input = modified_input
                .into_iter()
                .filter(|x| x.as_bytes()[i] as char == '0')
                .collect();
        }
    }
    let result_oxygen: u32 = u32::from_str_radix(&modified_input[0], 2).unwrap();

    modified_input = input.to_vec();
    for i in 0..modified_input.len() {
        if modified_input.len() == 1 {
            break;
        }
        if count_ones_in_column(&modified_input, i) * 2 < modified_input.len() {
            modified_input = modified_input
                .into_iter()
                .filter(|x| x.chars().nth(i) == Some('1'))
                .collect();
        } else {
            modified_input = modified_input
                .into_iter()
                .filter(|x| x.chars().nth(i) == Some('0'))
                .collect();
        }
    }
    let result_co2: u32 = u32::from_str_radix(&modified_input[0], 2).unwrap();

    result_oxygen * result_co2
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
