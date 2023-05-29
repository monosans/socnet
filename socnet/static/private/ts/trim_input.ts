const whiteSpaceRegex = /^\s+$/u;

function cleanWhitespaceInput(e: Event): void {
  const input = e.currentTarget! as HTMLInputElement;
  if (whiteSpaceRegex.test(input.value)) {
    input.value = "";
  }
}

for (const input of document.querySelectorAll(
  'input[type="text"], input:not([type]), textarea'
)) {
  input.addEventListener("input", cleanWhitespaceInput);
}
