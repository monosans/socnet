const options = { locale: document.documentElement.lang };

async function formatDates(parentNode: ParentNode): Promise<void> {
  const elements = parentNode.querySelectorAll<HTMLElement>("[data-epoch]");

  if (elements.length) {
    // eslint-disable-next-line @typescript-eslint/naming-convention
    const { DateTime } = await import(
      "https://cdn.jsdelivr.net/npm/luxon@3/+esm"
    );
    const relativeOptions = { base: DateTime.now() };
    for (const el of elements) {
      const dt = DateTime.fromSeconds(
        Number.parseInt(el.dataset["epoch"]!),
        options,
      );
      const relativeDt = dt.toRelative(relativeOptions);
      if (el.textContent !== relativeDt) {
        el.textContent = relativeDt;
      }
      if (!el.title) {
        el.title = dt.toLocaleString(DateTime.DATETIME_FULL);
      }
    }
  }
}

void (async function formatAllDates(): Promise<void> {
  await formatDates(document.body);
  setTimeout(formatAllDates, 1000);
})();

new MutationObserver((mutations) => {
  for (const mutation of mutations) {
    if (mutation.type === "childList") {
      void (async (): Promise<void> => {
        for (const node of mutation.addedNodes) {
          if (node instanceof Element) {
            // eslint-disable-next-line no-await-in-loop
            await formatDates(node);
          }
        }
      })();
    }
  }
}).observe(document.body, { childList: true, subtree: true });
