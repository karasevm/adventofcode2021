use std::collections::hash_map::Entry;
use std::collections::HashMap;
use std::collections::hash_set::HashSet;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::{env, vec};

fn count_paths(map: HashMap<&str, Vec<&str>>, next: &str, lowercase_seen: &HashSet<&str>, part: i32) -> i32 {
    if next == "end" { 
        return 1; 
    }
    let mut result = 0;
    let next_caves = &map[next];
    for cave in next_caves {
        if *cave == "start" { continue }
        let cave_is_lowercase = cave.chars().nth(0).unwrap().is_lowercase();
        if part == 1 && lowercase_seen.contains(cave) {
            continue;
        }
        let mut new_seen = lowercase_seen.clone();
        if cave_is_lowercase {  
            new_seen.insert(cave);
        } 
        result +=  count_paths(
            map.clone(),
            cave,
            &new_seen,
            if (part == 2 && lowercase_seen.contains(cave)) || part == 1 {1} else {2}
        )
    }
    result
}

fn get_cave_map(input: &Vec<String>) -> HashMap<&str, Vec<&str>> {
    let mut cave_map: HashMap<&str, Vec<&str>> = HashMap::new();
    for line in input {
        let caves: Vec<&str> = line.split("-").collect();

        match cave_map.entry(caves[0]) {
            Entry::Occupied(mut e) => {
                e.get_mut().push(caves[1]);
            }
            Entry::Vacant(e) => {
                e.insert(vec![caves[1]]);
            }
        }

        match cave_map.entry(caves[1]) {
            Entry::Occupied(mut e) => {
                e.get_mut().push(caves[0]);
            }
            Entry::Vacant(e) => {
                e.insert(vec![caves[0]]);
            }
        }
    }
    cave_map
}

fn part1(input: &Vec<String>) -> i32 {
    let map = get_cave_map(input);
    count_paths(map, "start", &HashSet::new(), 1)
}

fn part2(input: &Vec<String>) -> i32 {
    let map = get_cave_map(input);
    count_paths(map, "start", &HashSet::new(), 2)
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
