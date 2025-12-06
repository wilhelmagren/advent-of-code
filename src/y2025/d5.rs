use std::fs;
use std::ops;

pub fn p1(path: &str) -> String {
    let puzzle = fs::read_to_string(path).unwrap();
    let mut ranges: Vec<ops::Range<usize>> = Vec::new();

    for line in puzzle.lines() {
        if line == "" {}
        break;
    }

    todo!()
}

pub fn p2(path: &str) -> String {
    let puzzle = fs::read_to_string(path).unwrap();
    todo!()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn d5p1_example() {
        println!("d5p1 example: {}", p1("./res/2025/d5-example.txt"));
    }

    #[test]
    fn d5p2_example() {
        println!("d5p2 example: {}", p2("./res/2025/d5-example.txt"));
    }
}
