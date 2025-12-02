use std::fs;

// Invalid IDs are IDs which are made up uf some sequence of digits
// repeated twice, e.g., 55 (5 twice), 6464 (64 twice), 123123 (123 twice).
pub fn p1(path: &str) {
    let mut puzzle = fs::read_to_string(path).unwrap();
    let mut invalids: i64 = 0;

    // Remove trailing newline.
    _ = puzzle.pop();

    for id_range in puzzle.split(',') {
        let midpoint = id_range.find('-').unwrap();

        let lhs = id_range[..midpoint].parse::<i64>().unwrap();
        let rhs = id_range[(midpoint + 1)..].parse::<i64>().unwrap();

        for num in lhs..=rhs {
            let s = num.to_string();
            let cc = s.chars().count();

            if cc % 2 != 0 {
                continue;
            }

            let ln = &s[..(cc / 2)];
            let rn = &s[(cc / 2)..];

            if ln == rn {
                invalids += s.parse::<i64>().unwrap();
            }
        }
    }
    println!("d2p1: {}", invalids);
}

// Now an ID is invalid if it is only made only of some sequence of
// digits repeated at least twice. So 1234123 (1234 twice), 123123123 (123 three times),
// 1212121212 (12 five times), and 1111111 (1 seven times).
//
// If the length of the ID is 7 digits, the only invalid ID is XXXXXXX.
// If the length of the ID is 6 digits, we can have invalid IDs with sequences of length:
//  - 1
//  - 2
//  - 3
// If the length of the ID is 5 digits, we can have invalid IDs with sequences of length:
//  - 1
pub fn p2(path: &str) {
    let mut puzzle = fs::read_to_string(path).unwrap();
    let mut invalids: i64 = 0;

    // Remove trailing newline.
    _ = puzzle.pop();

    // Wtf is this solution?..
    // This is like O(n * (b - a) * c * ...)
    // For each id range we:
    //  - loop over all the numbers in the range,
    //  - go through all possible sequence lengths,
    //  - go through all possible repetitions of the sequence...
    //
    // Really stinky! But it works :)
    for id_range in puzzle.split(',') {
        let midpoint = id_range.find('-').unwrap();

        let lhs = id_range[..midpoint].parse::<i64>().unwrap();
        let rhs = id_range[(midpoint + 1)..].parse::<i64>().unwrap();

        for num in lhs..=rhs {
            let s = num.to_string();
            let cc = s.chars().count();

            let mut invalid_num: bool = false;

            // Sequence lengths
            for sl in 1..(cc as i64) {
                if invalid_num {
                    break;
                }

                // This is a seq len that can indicate invalid ID
                if (cc as i64) % sl == 0 {
                    let n_reps = (cc as i64) / sl;
                    let seq = &s[..(sl as usize)];

                    let mut can_seq_be_invalid = n_reps > 1;

                    for j in 1..n_reps {
                        let lr = (j * sl) as usize;
                        let rr = ((j + 1) * sl) as usize;

                        if can_seq_be_invalid && seq != &s[lr..rr] {
                            can_seq_be_invalid = false;
                        }
                    }

                    if can_seq_be_invalid {
                        invalid_num = true;
                        break;
                    }
                }
            }

            if invalid_num {
                invalids += s.parse::<i64>().unwrap();
            }
        }
    }
    println!("d2p2: {}", invalids);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_example() {
        p1("./res/d2-example.txt");
    }

    #[test]
    fn p2_example() {
        p2("./res/d2-example.txt");
    }
}
