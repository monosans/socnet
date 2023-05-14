"use strict";
(() => {
  const whiteSpaceRegex = /^\s+$/;

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

  const textInputSelectors = [
    'input[type="text"]',
    "input:not([type])",
    "textarea",
  ];
  for (const input of document.querySelectorAll(textInputSelectors)) {
    input.addEventListener("input", cleanWhitespaceInput);
  }
})();
