use once_cell::sync::Lazy;
use pyo3::prelude::*;
use std::collections::HashMap;

static AMMONIA: Lazy<ammonia::Builder> = Lazy::new(|| {
    let mut cleaner = ammonia::Builder::default();
    cleaner.set_tag_attribute_values(HashMap::from([
        ("img", HashMap::from([("loading", "lazy")])),
        ("table", HashMap::from([("class", "table")])),
    ]));
    cleaner
});

static CMARK_OPTIONS: Lazy<pulldown_cmark::Options> = Lazy::new(|| {
    let mut options = pulldown_cmark::Options::empty();
    options.insert(pulldown_cmark::Options::ENABLE_TABLES);
    options.insert(pulldown_cmark::Options::ENABLE_STRIKETHROUGH);
    options
});

#[pyfunction]
fn markdownify(text: &str) -> String {
    let parser = pulldown_cmark::Parser::new_ext(text, *CMARK_OPTIONS);
    let mut html = String::new();
    pulldown_cmark::html::push_html(&mut html, parser);
    AMMONIA.clean(&html).to_string()
}

#[pymodule]
fn socnet_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(markdownify, m)?)?;
    Ok(())
}
