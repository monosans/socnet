use compact_str::CompactString;
use pyo3::{prelude::*, pybacked::PyBackedStr, types::PyString};

#[pyfunction]
#[pyo3(signature = (value, /))]
pub fn normalize_str(
    py: Python<'_>,
    value: PyBackedStr,
) -> Bound<'_, PyString> {
    py.detach(|| {
        let normalized = normalize(&value);
        (normalized != *value).then_some(normalized)
    })
    .map_or_else(
        // Already normalized: hand back the original object without copying.
        || value.into_pyobject(py).unwrap_or_else(|e| match e {}),
        |normalized| PyString::new(py, &normalized),
    )
}

/// Collapses whitespace runs inside lines into single spaces, drops blank
/// lines and trims each line.
fn normalize(value: &str) -> CompactString {
    // The output is never longer than the input, and up to 24 bytes of it
    // fit inline without a heap allocation.
    let mut out = CompactString::with_capacity(value.len());

    for line in value.lines() {
        let mut words = line.split_whitespace();
        if let Some(first_word) = words.next() {
            if !out.is_empty() {
                out.push('\n');
            }
            out.push_str(first_word);
            for w in words {
                out.push(' ');
                out.push_str(w);
            }
        }
    }

    out
}

#[cfg(test)]
mod tests {
    use super::normalize;

    #[test]
    fn already_normalized() {
        for s in ["", "a", "a b", "a\nb c", "caf\u{e9} na\u{ef}ve\n\u{fc}ber"] {
            assert_eq!(normalize(s), s, "{s:?}");
        }
    }

    #[test]
    fn not_normalized() {
        for (s, expected) in [
            (" ", ""),
            ("\n", ""),
            ("a ", "a"),
            (" a", "a"),
            ("a\n", "a"),
            ("a  b", "a b"),
            ("a\tb", "a b"),
            ("a\rb", "a b"),
            ("a\r\nb", "a\nb"),
            ("a\n\nb", "a\nb"),
            ("a \nb", "a\nb"),
            ("a\n b", "a\nb"),
            ("a\u{a0}b", "a b"),
            ("a\u{3000}b", "a b"),
            ("caf\u{e9}  na\u{ef}ve", "caf\u{e9} na\u{ef}ve"),
            (
                "\n\n \tstring\t  \n\n\n   string  \tstring  \n  \t ",
                "string\nstring string",
            ),
        ] {
            assert_eq!(normalize(s), expected, "{s:?}");
        }
    }
}
