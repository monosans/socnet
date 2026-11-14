<!--
Pull requests are squash-merged, so write the title in the Conventional Commits
style: `fix: ...`, `feat: ...`, `docs: ...`, `refactor: ...`, `test: ...`, `chore: ...`.

CI runs the linters and tests. To catch failures before you push, run:

uvx prek run --all-files
docker compose run --rm django pytest
uv run --group typecheck --no-group dev --locked mypy .
npx oxlint
cd socnet_rs && cargo +nightly fmt --check && cargo +beta clippy --all-targets --
-->

## Summary

<!-- What does this change, and why? -->

## Related issues

<!-- `Closes #123` closes the issue on merge. Remove this section if there are none. -->

## Testing

<!-- How did you check that this works? -->

## Checklist

- [ ] New behavior has tests.
- [ ] `locale/ru/LC_MESSAGES/django.po` has Russian translations for new or changed strings.
