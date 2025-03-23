use pyo3::prelude::*;

const CFG: ::minify_html::Cfg = ::minify_html::Cfg {
    allow_noncompliant_unquoted_attribute_values: false,
    allow_optimal_entities: false,
    allow_removing_spaces_between_attributes: false,
    keep_closing_tags: false,
    keep_comments: false,
    keep_html_and_head_opening_tags: false,
    keep_input_type_text_attr: true,
    keep_ssi_comments: false,
    minify_css: false,
    minify_doctype: false,
    minify_js: false,
    preserve_brace_template_syntax: false,
    preserve_chevron_percent_template_syntax: false,
    remove_bangs: false,
    remove_processing_instructions: false,
};

#[pyfunction]
#[pyo3(signature = (value, /))]
pub(crate) fn minify_html(py: Python<'_>, value: &str) -> String {
    py.allow_threads(move || {
        let minified = ::minify_html::minify(value.as_bytes(), &CFG);
        String::from_utf8(minified).unwrap()
    })
}
