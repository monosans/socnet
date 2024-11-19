const formatter = new Intl.NumberFormat(document.documentElement.lang, {
  // @ts-expect-error
  notation: "compact",
});

function formatNumber(element: HTMLOrSVGElement & Node): void {
  const unformattedNumber = Number.parseInt(
    element.dataset["unformattedNumber"]!,
  );
  element.textContent = formatter.format(unformattedNumber);
}

for (const el of document.body.querySelectorAll<HTMLElement>(
  "[data-unformatted-number]",
)) {
  formatNumber(el);
}

new MutationObserver((mutations) => {
  for (const mutation of mutations) {
    if (mutation.type === "attributes") {
      if (
        mutation.attributeName === "data-unformatted-number" &&
        mutation.target instanceof HTMLElement
      ) {
        formatNumber(mutation.target);
      }
    } else if (mutation.type === "childList") {
      for (const node of mutation.addedNodes) {
        if (
          node instanceof HTMLElement &&
          node.matches("[data-unformatted-number]")
        ) {
          formatNumber(node);
        }
      }
    }
  }
}).observe(document.body, {
  attributeFilter: ["data-unformatted-number"],
  attributes: true,
  childList: true,
  subtree: true,
});
