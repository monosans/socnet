import { createRequire } from "node:module";

/*
 * Stylelint resolves `extends` like ESM imports, which ignore NODE_PATH, so the
 * configs installed in the pre-commit hook environment are resolved here.
 */
const require = createRequire(import.meta.url);

/** @type {import('stylelint').Config} */
const config = {
  extends: [
    require.resolve("stylelint-config-standard"),
    require.resolve("stylelint-config-recess-order"),
  ],
};

export default config;
