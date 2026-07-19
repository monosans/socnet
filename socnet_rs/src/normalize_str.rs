use pyo3::prelude::*;

#[pyfunction]
#[pyo3(signature = (value, /))]
pub fn normalize_str(
    py: Python<'_>,
    value: &str,
) -> compact_str::CompactString {
    py.detach(move || {
        let mut out = compact_str::CompactString::const_new("");
        let mut first_line = true;

        for line in value.lines() {
            let mut words = line.split_whitespace();
            if let Some(first_word) = words.next() {
                if first_line {
                    first_line = false;
                } else {
                    out.push('\n');
                }
                out.push_str(first_word);
                for w in words {
                    out.push(' ');
                    out.push_str(w);
                }
            }
        }

        out
    })
}
