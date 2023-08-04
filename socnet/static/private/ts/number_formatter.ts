const formatter = new Intl.NumberFormat(
  navigator.language === "ru" ? "ru" : "en",
  {
    // @ts-expect-error
    notation: "compact",
  },
);

export default function formatNumber(element: HTMLOrSVGElement & Node): void {
  const unformattedNumber = Number.parseInt(
    element.dataset["unformattedNumber"]!,
  );
  element.textContent = formatter.format(unformattedNumber);
}

for (const el of document.querySelectorAll<HTMLElement>(
  "[data-unformatted-number]",
)) {
  formatNumber(el);
}
