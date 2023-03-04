"use strict";
(() => {
  const whiteSpaceRegex = /^\s+$/;
  const textInputSelectors = [
    'input[type="text"]',
    "input:not([type])",
    "textarea",
  ];

  /**
   * @param {Event} e
   * @return {void}
   */
  function cleanWhitespaceInput(e) {
    const input = e.currentTarget;
    if (whiteSpaceRegex.test(input.value)) {
      input.value = "";
    }
  }

  const inputs = document.querySelectorAll(textInputSelectors);
  for (const input of inputs) {
    input.addEventListener("input", cleanWhitespaceInput);
  }

  /**
   * @param {Event} e
   * @return {void}
   */
  function trimInputs(e) {
    const inputs = e.currentTarget.querySelectorAll(textInputSelectors);
    for (const input of inputs) {
      input.value = input.value.trim();
    }
  }

  const forms = document.querySelectorAll("form");
  for (const form of forms) {
    form.addEventListener("submit", trimInputs);
  }
})();
