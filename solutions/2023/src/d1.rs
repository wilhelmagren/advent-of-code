use std::fs;

pub fn d1p1(path: &str) -> u32 {
    fs::read_to_string(path)
        .expect("Could not read data file.")
        .lines()
        .map(|l| {
            l.chars()
                .filter(|c| c.is_digit(10))
                .map(|c| {
                    c.to_digit(10)
                        .unwrap()
                })
                .collect::<Vec<u32>>()
        })
        .map(|v| {
            10 * v.first().unwrap() + v.last().unwrap()
        })
        .sum()
}

pub fn d1p2(path: &str) -> u32 {
    fs::read_to_string(path)
        .expect("Could not read data file.")
        .lines()
        .map(|l| {
            l.to_string()
                .replace("one", "one1one")
                .replace("two", "two2two")
                .replace("three", "three3three")
                .replace("four", "four4four")
                .replace("five", "five5five")
                .replace("six", "six6six")
                .replace("seven", "seven7seven")
                .replace("eight", "eight8eight")
                .replace("nine", "nine9nine")
                .chars()
                .filter(|c| c.is_digit(10))
                .map(|c| {
                    c.to_digit(10)
                        .unwrap()
                })
                .collect::<Vec<u32>>()
        })
        .map(|v| {
            10 * v.first().unwrap() + v.last().unwrap()
        })
        .sum()
}

#[cfg(test)]
mod tests_d1 {
    use super::*;

    #[test]
    fn test_part1() {
        let solution = d1p1("./data/d1t1.txt");
        assert_eq!(142, solution);
    }

    #[test]
    fn test_part2() {
        let solution = d1p2("./data/d1t2.txt");
        assert_eq!(281, solution);
    }
}
