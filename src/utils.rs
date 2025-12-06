/// Get the maxinum number (char) in the slize, but if multiple
/// maximum then get the one with the lowest index.
pub fn max_in_slice(s: &str) -> (usize, char) {
    let mut bidx: usize = 0;
    let mut bnum: char = '0';
    for (i, c) in s.chars().into_iter().enumerate() {
        if c > bnum {
            bnum = c;
            bidx = i;
        }
    }
    (bidx, bnum)
}
