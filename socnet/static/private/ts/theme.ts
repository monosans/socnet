const themeSwitcher = document.querySelector("#themeSwitcher")!;
const currentThemeIcon = document.querySelector("#currentThemeIcon")!;

function getTheme(): "auto" | "dark" | "light" {
  const storedTheme = localStorage.getItem("theme");
  return storedTheme === "light" || storedTheme === "dark"
    ? storedTheme
    : "auto";
}

function getAutoTheme(): "dark" | "light" {
  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

function setTheme(theme: string): void {
  document.documentElement.dataset["bsTheme"] =
    theme === "auto" ? getAutoTheme() : theme;

  const activeDropdown = themeSwitcher.querySelector(".dropdown-item.active")!;
  const activeDropdownIcon = activeDropdown.querySelector("i")!;

  const dropdownToActivate = themeSwitcher.querySelector(
    `[data-bs-theme-value="${theme}"]`
  )!;
  const dropdownToActivateIcon = dropdownToActivate.querySelector("i")!;

  activeDropdown.classList.remove("active");
  dropdownToActivate.classList.add("active");

  activeDropdownIcon.classList.add("text-primary");
  currentThemeIcon.className = dropdownToActivateIcon.className;
  dropdownToActivateIcon.classList.remove("text-primary");
}

setTheme(getTheme());
window
  .matchMedia("(prefers-color-scheme: dark)")
  .addEventListener("change", () => setTheme(getTheme()));

function toggleHandler(e: Event): void {
  const theme = (e.currentTarget! as HTMLElement).dataset["bsThemeValue"]!;
  localStorage.setItem("theme", theme);
  setTheme(theme);
}

for (const toggle of themeSwitcher.querySelectorAll("[data-bs-theme-value]")) {
  toggle.addEventListener("click", toggleHandler);
}
