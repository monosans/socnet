const formatter = new Intl.NumberFormat(
  navigator.language === "ru" ? "ru" : "en",
  {
    notation: "compact",
  }
);

/**
 * @param {Node & HTMLOrSVGElement} element
 * @return {void}
 */
export default function formatNumber(element) {
  const unformattedNumber = parseInt(element.dataset.unformattedNumber);
  element.textContent = formatter.format(unformattedNumber);
}

document.querySelectorAll("[data-unformatted-number]").forEach(formatNumber);
