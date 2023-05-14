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

  for (const input of document.querySelectorAll([
    'input[type="text"]',
    "input:not([type])",
    "textarea",
  ])) {
    input.addEventListener("input", cleanWhitespaceInput);
  }
})();
