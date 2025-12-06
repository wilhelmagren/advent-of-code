use std::fmt;
use std::time;

mod y2025;

pub mod utils;

struct Timer {
    inner: time::Instant,
}

impl Timer {
    pub fn new() -> Self {
        Self {
            inner: time::Instant::now(),
        }
    }

    pub fn start(&mut self) {
        self.inner = time::Instant::now();
    }

    pub fn elapsed(&self) -> f64 {
        self.inner.elapsed().as_secs_f64()
    }
}

struct ProblemResult {
    problem: String,
    solution: String,
    timing: f64,
}

impl ProblemResult {
    pub fn new(problem: String, solution: String, timing: f64) -> Self {
        Self {
            problem,
            solution,
            timing,
        }
    }
}

impl fmt::Display for ProblemResult {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let (value, unit) = if self.timing < 1e-3 {
            (self.timing * 1_000_000.0, "µs")
        } else {
            (self.timing * 1_000.0, "ms")
        };

        let timing_str = format!("{:.1}{}", value, unit);

        write!(
            f,
            "{:^22} {:>18} {:^20}",
            self.problem, self.solution, timing_str,
        )
    }
}

fn main() {
    println!("{:^22} {:^18} {:^20}", "Problem", "Solution", "Timing");
    println!("==================================================================");
    let mut timer = Timer::new();

    timer.start();
    println!(
        "{}",
        ProblemResult::new(
            "2025 Day 1 Part 1".to_string(),
            y2025::d1::p1("./res/2025/d1.txt"),
            timer.elapsed(),
        )
    );

    timer.start();
    println!(
        "{}",
        ProblemResult::new(
            "2025 Day 1 Part 2".to_string(),
            y2025::d1::p2("./res/2025/d1.txt"),
            timer.elapsed(),
        )
    );

    timer.start();
    println!(
        "{}",
        ProblemResult::new(
            "2025 Day 2 Part 1".to_string(),
            y2025::d2::p1("./res/2025/d2.txt"),
            timer.elapsed(),
        )
    );

    timer.start();
    println!(
        "{}",
        ProblemResult::new(
            "2025 Day 2 Part 2".to_string(),
            y2025::d2::p2("./res/2025/d2.txt"),
            timer.elapsed(),
        )
    );

    timer.start();
    println!(
        "{}",
        ProblemResult::new(
            "2025 Day 3 Part 1".to_string(),
            y2025::d3::p1("./res/2025/d3.txt"),
            timer.elapsed(),
        )
    );

    timer.start();
    println!(
        "{}",
        ProblemResult::new(
            "2025 Day 3 Part 2".to_string(),
            y2025::d3::p2("./res/2025/d3.txt"),
            timer.elapsed(),
        )
    );

    println!("==================================================================");
}
