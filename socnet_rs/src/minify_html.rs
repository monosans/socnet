use pyo3::prelude::*;

const CFG: ::minify_html::Cfg = ::minify_html::Cfg {
    do_not_minify_doctype: true,
    ensure_spec_compliant_unquoted_attribute_values: true,
    keep_closing_tags: false,
    keep_html_and_head_opening_tags: false,
    keep_spaces_between_attributes: true,
    keep_comments: false,
    minify_css: true,
    minify_css_level_1: false,
    minify_css_level_2: false,
    minify_css_level_3: false,
    minify_js: true,
    remove_bangs: false,
    remove_processing_instructions: false,
};

#[pyfunction]
pub fn minify_html(py: Python, value: &str) -> String {
    py.allow_threads(move || {
        let minified = ::minify_html::minify(value.as_bytes(), &CFG);
        String::from_utf8(minified).unwrap()
    })
}
