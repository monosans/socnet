//! Rust helpers for socnet: rendering Markdown to HTML and normalizing strings,
//! exposed to Python as the `socnet_rs` module.

mod markdownify;
mod normalize_str;

use pyo3::prelude::*;

#[pymodule]
mod socnet_rs {
    #[pymodule_export]
    use crate::{markdownify::markdownify, normalize_str::normalize_str};
}
