mod markdownify;
mod minify_html;
mod normalize_str;

use pyo3::prelude::*;

#[pymodule]
fn socnet_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(markdownify::markdownify, m)?)?;
    m.add_function(wrap_pyfunction!(crate::minify_html::minify_html, m)?)?;
    m.add_function(wrap_pyfunction!(normalize_str::normalize_str, m)?)?;
    Ok(())
}
