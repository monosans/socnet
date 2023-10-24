// eslint-disable-next-line @typescript-eslint/naming-convention
import Viewer from "https://cdn.jsdelivr.net/npm/viewerjs@1/+esm";

new Viewer(document.querySelector("#avatar")!, {
  button: false,
  navbar: false,
});
