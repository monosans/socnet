const options = { locale: navigator.language === "ru" ? "ru" : "en" };

/**
 * @return {void}
 */
function formatDates() {
  /**
   * @type {NodeListOf<HTMLElement>}
   */
  const elements = document.querySelectorAll("[data-epoch]");

  if (!elements.length) {
    return;
  }

  import("https://cdn.jsdelivr.net/npm/luxon@3/+esm").then(({ DateTime }) => {
    const relativeOptions = { base: DateTime.now() };
    for (const el of elements) {
      const dt = DateTime.fromSeconds(parseInt(el.dataset.epoch), options);
      const relativeDt = dt.toRelative(relativeOptions);
      if (el.textContent !== relativeDt) {
        el.textContent = relativeDt;
      }
      if (!el.title) {
        el.title = dt.toLocaleString(DateTime.DATETIME_FULL);
      }
    }
  });
}

formatDates();
setInterval(formatDates, 1000);
