use std::collections::HashMap;

use once_cell::sync::Lazy;
use pyo3::prelude::*;

static AMMONIA: Lazy<ammonia::Builder> = Lazy::new(|| {
    let mut cleaner = ammonia::Builder::default();
    cleaner.set_tag_attribute_values(HashMap::from([
        (
            "a",
            HashMap::from([(
                "class",
                "link-underline link-underline-opacity-0 \
                 link-underline-opacity-100-hover",
            )]),
        ),
        (
            "img",
            HashMap::from([
                ("class", "rounded"),
                ("loading", "lazy"),
                ("role", "button"),
            ]),
        ),
        ("table", HashMap::from([("class", "table w-auto")])),
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
pub fn markdownify(py: Python, text: &str) -> String {
    py.allow_threads(move || {
        let html = {
            let parser = pulldown_cmark::Parser::new_ext(text, *CMARK_OPTIONS);
            let mut html = String::new();
            pulldown_cmark::html::push_html(&mut html, parser);
            html
        };
        AMMONIA.clean(&html).to_string()
    })
}
