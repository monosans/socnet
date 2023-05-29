import Viewer from "https://cdn.jsdelivr.net/npm/viewerjs@1/+esm";

for (const container of document.querySelectorAll<HTMLElement>(
  ".markdown-container"
)) {
  new Viewer(container, { button: false });
}
