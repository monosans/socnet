import Viewer from "viewerjs";

import { requiredElement } from "../../dom";

new Viewer(requiredElement("#avatar", HTMLElement), {
  button: false,
  navbar: false,
});
