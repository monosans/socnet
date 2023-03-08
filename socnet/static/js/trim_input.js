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

  for (const input of document.querySelectorAll(textInputSelectors)) {
    input.addEventListener("input", cleanWhitespaceInput);
  }

  /**
   * @param {Event} e
   * @return {void}
   */
  function trimInputs(e) {
    for (const input of e.currentTarget.querySelectorAll(textInputSelectors)) {
      input.value = input.value.trim();
    }
  }

  for (const form of document.querySelectorAll("form")) {
    form.addEventListener("submit", trimInputs);
  }
})();
