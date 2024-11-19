import Viewer from "https://cdn.jsdelivr.net/npm/viewerjs@1/+esm";

function initializeViewer(element: HTMLElement): void {
  new Viewer(element, { button: false });
}

for (const container of document.body.querySelectorAll<HTMLElement>(
  ".markdown-container",
)) {
  initializeViewer(container);
}

new MutationObserver((mutations) => {
  for (const mutation of mutations) {
    if (mutation.type === "childList") {
      for (const node of mutation.addedNodes) {
        if (
          node instanceof HTMLElement &&
          node.matches(".markdown-container")
        ) {
          initializeViewer(node);
        }
      }
    }
  }
}).observe(document.body, {
  childList: true,
  subtree: true,
});
