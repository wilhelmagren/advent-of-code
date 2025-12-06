use std::fs;

use crate::utils::max_in_slice;

pub fn p1(path: &str) -> String {
    let puzzle = fs::read_to_string(path).unwrap();
    let mut joltage: i64 = 0;
    for line in puzzle.lines() {
        let mut a = i64::MIN;
        let mut b = i64::MIN;
        let mut aidx = 0;
        let mut bidx = 0;

        // we know its 1 byte size chars so we can do .len()
        // here instead of line.chars().count().
        let cc = line.len();

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

    joltage.to_string()
}

// The joltage output for the bank is still the number formed by the digits
// of the batteries you've turned on; the only difference is that now there
// will be 12 digits in each bank's joltage output instead of two.
pub fn p2(path: &str) -> String {
    let puzzle = fs::read_to_string(path).unwrap();
    let mut joltage: usize = 0;

    let mut numbers: Vec<char> = Vec::with_capacity(12);
    // Lets do a greedy algorithm where we aim to find the largest number in a
    // given slice. Again we can have two "pointers", left one starts at 0 and
    // then right one starts at line.len() - 12, for each slice that we find the
    // largest number in we move the left pointer to the index of the largest
    // number and increment the right pointer by 1.
    //
    //
    // Assume instead we need to find 3 digits to find in the sequence (10 long).
    // +---------------------------------------+
    // | 6 | 9 | 4 | 5 | 3 | 7 | 3 | 1 | 8 | 7 |
    // +---------------------------------------+
    //
    // First we aim to find the largest number in the slice [9, 6, 4, 5, 3, 7, 3, 1]
    // +---------------------------------------+
    // | 6 | 9 | 4 | 5 | 3 | 7 | 3 | 1 | 8 | 7 |
    // +---------------------------------------+
    //   |                           |
    // lidx                         ridx
    //
    // The number 9 is the largest at index 1. We have found one number,
    // now we still need to find 2 more numbers in the slice
    // +-------------------------------+
    // | 4 | 5 | 3 | 7 | 3 | 1 | 8 | 7 |
    // +-------------------------------+
    //
    // Our left pointer should be lidx=2, which was lidx + max_num_idx + 1
    // and the right pointer should just be incremented by one.
    // +---------------------------------------+
    // | 6 | 9 | 4 | 5 | 3 | 7 | 3 | 1 | 8 | 7 |
    // +---------------------------------------+
    //           |                       |
    //          lidx                    ridx
    //
    // The number 8 is the largest ad (in-slice) index 6.
    // update lidx = lidx + 6 + 1 and increment ridx by one.
    // lidx = 2 + 6 + 1 = 9, ridx = 9
    // +---+
    // | 7 |
    // +---+
    //   |
    // lidx, ridx
    //
    // What's the largest number in this slice? 7.
    // So the largest number we could find was 987.
    //

    for line in puzzle.lines() {
        let mut lidx: usize = 0;
        let mut ridx: usize = line.len() - 12;

        while numbers.len() < 12 {
            let (max_idx, num) = max_in_slice(&line[lidx..=ridx]);
            lidx += max_idx + 1;
            ridx += 1;
            numbers.push(num);
        }

        let s = numbers.iter().collect::<String>();
        joltage += s.parse::<usize>().unwrap();
        numbers.clear();
    }

    joltage.to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn d3p1_example() {
        println!("d3p1 example: {}", p1("./res/2025/d3-example.txt"));
    }

    #[test]
    fn d3p2_example() {
        println!("d3p2 example: {}", p2("./res/2025/d3-example.txt"));
    }
}
