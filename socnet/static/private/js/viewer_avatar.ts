import Viewer from "viewerjs";

import { requiredElement } from "../../dom";

// oxlint-disable-next-line no-new -- the viewer binds itself to the element on construction
new Viewer(requiredElement("#avatar", HTMLElement), { button: false, navbar: false });
