use std::fs;

pub fn p1(path: &str) {
    let puzzle = fs::read_to_string(path).unwrap();
    let mut joltage: i64 = 0;
    for line in puzzle.lines() {
        let mut a = i64::MIN;
        let mut b = i64::MIN;
        let mut aidx = 0;
        let mut bidx = 0;

        let cc = line.chars().count();

        for (idx, n) in line
            .chars()
            .map(|c| c.to_digit(10).unwrap() as i64)
            .enumerate()
        {
            // If we are not on the last number in the sequence then
            // we always want to replace our 'a' number with a larger
            // number.
            //
            // However, if it is the last number in the sequence then we
            // can't know that this number will be greater.
            if n > a && idx < (cc - 1) {
                a = n;
                b = i64::MIN;
                aidx = idx;
                continue;
            }

            if n > b {
                b = n;
                bidx = idx;
            }
        }

        if aidx < bidx {
            joltage += (a * 10) + b;
        } else {
            joltage += (b * 10) + a;
        }
    }

    println!("d3p1: {}", joltage);
}

// The joltage output for the bank is still the number formed by the digits
// of the batteries you've turned on; the only difference is that now there
// will be 12 digits in each bank's joltage output instead of two.
pub fn p2(path: &str) {
    let puzzle = fs::read_to_string(path).unwrap();
    let mut joltage: i64 = 0;
    let mut joltcola: Vec<char> = Vec::with_capacity(12);

    for line in puzzle.lines() {
        let mut prev_n = i64::MIN;

        for (idx, (c, n)) in line
            .chars()
            .map(|c| (c, c.to_digit(10).unwrap() as i64))
            .enumerate()
        {
        }

        println!("{:?}", joltcola);
        joltage += String::from_iter(&joltcola).parse::<i64>().unwrap();
        joltcola.clear();
    }

    println!("d3p2: {}", joltage);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_example() {
        p1("./res/d3-example.txt");
    }

    #[test]
    fn p2_example() {
        p2("./res/d3-example.txt");
    }
}
