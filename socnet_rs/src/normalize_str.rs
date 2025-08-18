use itertools::Itertools as _;
use pyo3::prelude::*;

#[pyfunction]
#[pyo3(signature = (value, /))]
pub fn normalize_str(py: Python<'_>, value: &str) -> String {
    py.allow_threads(move || {
        value
            .lines()
            .filter_map(|line| {
                if line.trim().is_empty() {
                    None
                } else {
                    Some(line.split_whitespace().join(" "))
                }
            })
            .join("\n")
    })
}
