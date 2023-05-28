import Viewer from "https://cdn.jsdelivr.net/npm/viewerjs@1/+esm";

/**
 * @param {ParentNode} parentNode
 * @return {void}
 */
export default (parentNode) => {
  new Viewer(parentNode, { button: false });
};
