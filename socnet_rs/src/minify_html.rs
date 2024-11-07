use pyo3::prelude::*;

const CFG: ::minify_html::Cfg = ::minify_html::Cfg {
    do_not_minify_doctype: true,
    ensure_spec_compliant_unquoted_attribute_values: true,
    keep_closing_tags: false,
    keep_html_and_head_opening_tags: false,
    keep_spaces_between_attributes: true,
    keep_comments: false,
    keep_input_type_text_attr: true,
    keep_ssi_comments: false,
    preserve_brace_template_syntax: false,
    preserve_chevron_percent_template_syntax: false,
    minify_css: false,
    minify_js: false,
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
