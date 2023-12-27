use pyo3::prelude::*;

const CFG: ::minify_html::Cfg = ::minify_html::Cfg {
    preserve_brace_template_syntax: true,
    ..crate::minify_html::CFG
};

#[pyfunction]
#[pyo3(signature = (value, /))]
pub(crate) fn minify_template(py: Python, value: &str) -> String {
    py.allow_threads(move || {
        let minified = ::minify_html::minify(value.as_bytes(), &CFG);
        String::from_utf8(minified).unwrap()
    })
}
