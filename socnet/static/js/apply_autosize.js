"use strict";
(() => {
  const textareas = document.getElementsByTagName("textarea");
  for (const textarea of textareas) {
    textarea.rows = 1;
  }
  autosize(textareas);
})();
