const themeSwitcher = document.querySelector("#themeSwitcher")!;
const currentThemeIcon = document.querySelector("#currentThemeIcon")!;

function getStoredOrDefaultTheme(): "dark" | "light" {
  const storedTheme = localStorage.getItem("theme");
  if (storedTheme === "dark" || storedTheme === "light") {
    return storedTheme;
  }
  return globalThis.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

function setTheme(): void {
  const theme = getStoredOrDefaultTheme();
  document.documentElement.dataset["bsTheme"] = theme;

  const activeDropdown = themeSwitcher.querySelector(".dropdown-item.active")!;
  const activeDropdownIcon = activeDropdown.querySelector("i")!;

  const dropdownToActivate = themeSwitcher.querySelector(
    `[data-bs-theme-value="${theme}"]`,
  )!;
  const dropdownToActivateIcon = dropdownToActivate.querySelector("i")!;

  activeDropdown.classList.remove("active");
  dropdownToActivate.classList.add("active");

  activeDropdownIcon.classList.add("text-primary");
  currentThemeIcon.className = dropdownToActivateIcon.className;
  dropdownToActivateIcon.classList.remove("text-primary");
}

setTheme();

globalThis
  .matchMedia("(prefers-color-scheme: dark)")
  .addEventListener("change", setTheme);

globalThis.addEventListener("storage", (e) => {
  if (e.key === "theme") {
    setTheme();
  }
});

document.body.addEventListener("click", (e) => {
  const btn = (e.target as Element).closest<HTMLElement>(
    "[data-bs-theme-value]",
  );
  if (!btn) {
    return;
  }
  const theme = btn.dataset["bsThemeValue"]!;
  localStorage.setItem("theme", theme);
  setTheme();
});
