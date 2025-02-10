/* eslint-disable @typescript-eslint/naming-convention */

/** @type {import('stylelint').Config} */
export default {
  extends: ["stylelint-config-standard", "stylelint-config-recess-order"],
  rules: { "color-function-notation": "legacy" },
};
