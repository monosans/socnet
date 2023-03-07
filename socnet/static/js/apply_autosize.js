"use strict";
(() => {
  const textareas = document.getElementsByTagName("textarea");
  for (const textarea of textareas) {
    textarea.rows = 1;
  }
  // eslint-disable-next-line no-undef
  autosize(textareas);
})();
