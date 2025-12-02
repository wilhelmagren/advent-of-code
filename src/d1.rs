use std::fs;

enum Direction {
    Left,
    Right,
}

impl Direction {
    pub fn from_str(s: &str) -> Self {
        match s {
            "L" => Direction::Left,
            "R" => Direction::Right,
            _ => panic!("invalid direction"),
        }
    }
}

struct Rotation {
    dir: Direction,
    amount: i32,
}

impl Rotation {
    pub fn from_line(l: &str) -> Self {
        let dir = Direction::from_str(&l[..1]);
        let amount: i32 = l[1..].parse::<i32>().unwrap();
        Rotation { dir, amount }
    }

    pub fn signed_amount(&self) -> i32 {
        match self.dir {
            Direction::Left => -self.amount,
            Direction::Right => self.amount,
        }
    }
}

// Turning the dial left from 0 one click makes it point to 99,
// turning the dial right from 99 one click makes it point to 0.
// Count the number of the times the dial is pointing at 0.
//
// Rust modulu '%' is not modulu, heh, it is remainder...
// But we can use the `rem_euclid` method to calculate what we are after.
pub fn p1(path: &str) {
    let puzzle = fs::read_to_string(path).unwrap();
    let mut dial: i32 = 50;
    let mut cnt: i32 = 0;

    for line in puzzle.lines() {
        let r = Rotation::from_line(line);
        let sa = r.signed_amount();

        dial = (dial + sa).rem_euclid(100);

        if dial == 0 {
            cnt += 1;
        }
    }
    println!("d1p1: {}", cnt);
}

/// Now also count each time the dial 'goes over' 0,
/// each time! Because it can rotate many full times.
pub fn p2(path: &str) {
    let puzzle = fs::read_to_string(path).unwrap();
    let mut dial: i32 = 50;
    let mut cnt: i32 = 0;

    for line in puzzle.lines() {
        let r = Rotation::from_line(line);
        let sa = r.signed_amount();
        let was_zero = dial == 0;

        // count number of full rotations, this is ugly
        // why not just do remainder and full-num div?
        /*
        while sa.abs() > 100 {
            cnt += 1;
            if sa < 0 {
                sa += 100;
            } else {
                sa -= 100;
            }
        }
        */

        // yea this is a real gamer moment
        cnt += (sa / 100).abs();
        dial += sa % 100;

        if dial > 100 || (dial < 0 && !was_zero) {
            cnt += 1;
        }

        dial = dial.rem_euclid(100);

        if dial == 0 {
            cnt += 1;
        }
    }

    println!("d1p2: {}", cnt);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_example() {
        p1("./res/d1-example.txt");
    }

    #[test]
    fn p2_example() {
        p2("./res/d1-example.txt");
    }
}
