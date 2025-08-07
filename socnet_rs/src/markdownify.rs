use std::{collections::HashMap, sync::LazyLock};

use pyo3::prelude::*;

static AMMONIA: LazyLock<ammonia::Builder<'_>> = LazyLock::new(|| {
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

const CMARK_OPTIONS: pulldown_cmark::Options =
    pulldown_cmark::Options::ENABLE_TABLES
        .union(pulldown_cmark::Options::ENABLE_STRIKETHROUGH);

#[pyfunction]
#[pyo3(signature = (value, /))]
pub fn markdownify(py: Python<'_>, value: &str) -> String {
    py.allow_threads(move || {
        let parser = pulldown_cmark::Parser::new_ext(value, CMARK_OPTIONS);
        let mut html = String::new();
        pulldown_cmark::html::push_html(&mut html, parser);
        AMMONIA.clean(&html).to_string()
    })
}
