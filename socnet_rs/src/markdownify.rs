use std::{collections::HashMap, sync::LazyLock};

use pyo3::{prelude::*, types::PyString};

type Attributes = [(&'static str, &'static str)];

const LINK_ATTRIBUTES: &Attributes =
    &[("class", "link-underline link-underline-opacity-0 link-underline-opacity-100-hover")];
const IMAGE_ATTRIBUTES: &Attributes =
    &[("class", "rounded"), ("loading", "lazy"), ("role", "button")];
const TABLE_ATTRIBUTES: &Attributes = &[("class", "table w-auto")];
const LINK_REL: &str = "noopener noreferrer";

static AMMONIA: LazyLock<ammonia::Builder<'_>> = LazyLock::new(|| {
    let mut cleaner = ammonia::Builder::default();
    cleaner
        .set_tag_attribute_values(HashMap::from([
            ("a", HashMap::from_iter(LINK_ATTRIBUTES.iter().copied())),
            ("img", HashMap::from_iter(IMAGE_ATTRIBUTES.iter().copied())),
            ("table", HashMap::from_iter(TABLE_ATTRIBUTES.iter().copied())),
        ]))
        .link_rel(Some(LINK_REL));
    cleaner
});

/// Length of ` name="value"` for each of `attributes`.
const fn attributes_len(attributes: &Attributes) -> usize {
    match attributes {
        [] => 0,
        [(name, value), rest @ ..] => name
            .len()
            .saturating_add(value.len())
            .saturating_add(r#" ="""#.len())
            .saturating_add(attributes_len(rest)),
    }
}

/// How much longer `AMMONIA` makes each tag.
const TAG_GROWTH: [(pulldown_cmark::TagEnd, usize); 3] = [
    (
        pulldown_cmark::TagEnd::Link,
        attributes_len(LINK_ATTRIBUTES).saturating_add(attributes_len(&[("rel", LINK_REL)])),
    ),
    // Without the ` /` that pulldown-cmark closes `<img />` with.
    (pulldown_cmark::TagEnd::Image, attributes_len(IMAGE_ATTRIBUTES).saturating_sub(" /".len())),
    (pulldown_cmark::TagEnd::Table, attributes_len(TABLE_ATTRIBUTES)),
];

const CMARK_OPTIONS: pulldown_cmark::Options =
    pulldown_cmark::Options::ENABLE_TABLES.union(pulldown_cmark::Options::ENABLE_STRIKETHROUGH);

#[pyfunction]
#[pyo3(signature = (value, /))]
pub fn markdownify<'py>(py: Python<'py>, value: &str) -> PyResult<Bound<'py, PyString>> {
    let out = py.detach(|| {
        let (html, growth) = to_html(value);
        // Sanitizing mostly keeps the HTML as is, apart from the attributes
        // it adds.
        let mut out = Vec::with_capacity(html.len().saturating_add(growth));
        // `Document::to_string` serializes into a buffer and then copies it
        // into a `String`; writing straight into a buffer skips that copy.
        AMMONIA.clean(&html).write_to(&mut out).map(|()| out)
    })?;
    PyString::from_bytes(py, &out)
}

/// Renders `value` to HTML, and counts how much longer `AMMONIA` makes the
/// tags it rendered.
fn to_html(value: &str) -> (String, usize) {
    // Over a corpus of messages, HTML is up to 1.5 times longer than its
    // Markdown, plus the tags of a short paragraph.
    let mut html = String::with_capacity(
        value.len().saturating_add(value.len().div_euclid(2)).saturating_add(32),
    );
    let mut growth = 0_usize;
    let parser = pulldown_cmark::Parser::new_ext(value, CMARK_OPTIONS).inspect(|event| {
        if let pulldown_cmark::Event::End(end) = event
            && let Some(&(_, tag_growth)) = TAG_GROWTH.iter().find(|(tag, _)| tag == end)
        {
            growth = growth.saturating_add(tag_growth);
        }
    });
    pulldown_cmark::html::push_html(&mut html, parser);
    (html, growth)
}

#[cfg(test)]
mod tests {
    use super::{AMMONIA, to_html};

    #[test]
    fn growth_matches_ammonia() {
        for value in [
            "text",
            "[link](https://example.com)",
            "![image](https://example.com/a.png)",
            "| a |\n| - |\n| b |",
            "[a](https://a.com) ![b](https://b.com/b.png) [c](https://c.com)",
        ] {
            let (html, growth) = to_html(value);
            let cleaned = AMMONIA.clean(&html).to_string();
            assert_eq!(cleaned.len(), html.len() + growth, "{value:?}");
        }
    }
}
