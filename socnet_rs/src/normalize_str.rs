use pyo3::prelude::*;

#[pyfunction]
pub fn normalize_str(py: Python, value: &str) -> String {
    py.allow_threads(move || {
        value
            .lines()
            .filter(|line| !line.trim().is_empty())
            .map(|line| line.split_whitespace().collect::<Vec<_>>().join(" "))
            .collect::<Vec<_>>()
            .join("\n")
    })
}
