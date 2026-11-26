// Browsers without `field-sizing` (see bootstrap.css) get the library as a fallback.
async function autosizeTextareas(): Promise<void> {
  if (CSS.supports("field-sizing", "content")) {
    return;
  }
  const { default: autosize } = await import("autosize");
  autosize(document.body.querySelectorAll("textarea"));
}

void autosizeTextareas();
