import { createRequire } from "node:module";

/*
 * Stylelint resolves `extends` like ESM imports, which ignore NODE_PATH, so the
 * packages installed in the pre-commit hook environment are resolved here.
 */
const require = createRequire(import.meta.url);

/** @type {import('stylelint').Config} */
const config = {
  extends: [
    require.resolve("stylelint-config-standard"),
    require.resolve("stylelint-config-recess-order"),
  ],
  // Where the --bs-* custom properties are declared: the Bootstrap build bootstrap.css imports.
  referenceFiles: require.resolve("bootstrap/dist/css/bootstrap.min.css"),
  reportDescriptionlessDisables: true,
  reportInvalidScopeDisables: true,
  reportNeedlessDisables: true,
  reportUnscopedDisables: true,
  rules: {
    "color-no-invalid-hex": true,
    "function-linear-gradient-no-nonstandard-direction": true,
    "function-no-unknown": true,
    "function-url-no-scheme-relative": true,
    "no-unknown-animations": true,
    "no-unknown-custom-media": true,
    "no-unknown-custom-properties": true,
    "unit-no-unknown": true,
  },
};

export default config;
