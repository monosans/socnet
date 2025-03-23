use pyo3::prelude::*;

#[pyfunction]
#[pyo3(signature = (value, /))]
pub(crate) fn minify_html(py: Python<'_>, value: &str) -> String {
    py.allow_threads(move || {
        let minified = ::minify_html::minify(
            value.as_bytes(),
            &::minify_html::Cfg::default(),
        );
        String::from_utf8(minified).unwrap()
    })
}
