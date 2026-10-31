<!--
Pull requests are squash-merged, so write the title in the Conventional Commits
style: `fix: ...`, `feat: ...`, `docs: ...`, `refactor: ...`, `test: ...`, `chore: ...`.
-->

## Summary

<!-- What does this change, and why? -->

## Related issues

<!-- `Closes #123` closes the issue on merge. Remove this section if there are none. -->

## Testing

<!-- How did you check that this works? -->

## Checklist

- [ ] `uvx prek run --all-files` passes.
- [ ] `docker compose run --rm django pytest` passes, and new behavior has tests.
- [ ] `uv run --group typecheck --no-group dev --locked mypy .` passes, if Python code changed.
- [ ] `npx eslint --max-warnings 0 .` and `npx tsc --build --noEmit` pass, if the frontend changed.
- [ ] `cargo +nightly fmt --check` and `cargo +beta clippy --` pass in `socnet_rs/`, if Rust code changed.
- [ ] Migrations are included for any model change.
- [ ] `locale/ru/LC_MESSAGES/django.po` has Russian translations for new or changed strings.
