const formatter = new Intl.NumberFormat(
  navigator.language === "ru" ? "ru" : "en",
  {
    // @ts-expect-error
    notation: "compact",
  },
);

export default function formatNumber(element: HTMLOrSVGElement & Node): void {
  const unformattedNumber = parseInt(element.dataset["unformattedNumber"]!);
  element.textContent = formatter.format(unformattedNumber);
}

document
  .querySelectorAll<HTMLElement>("[data-unformatted-number]")
  .forEach(formatNumber);
