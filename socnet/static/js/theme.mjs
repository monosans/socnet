const themeSwitcher = document.querySelector("#themeSwitcher");
const currentThemeIcon = document.querySelector("#currentThemeIcon");

/**
 * @return {string}
 */
function getTheme() {
  const storedTheme = localStorage.getItem("theme");
  return ["light", "dark"].includes(storedTheme) ? storedTheme : "auto";
}

/**
 * @return {string}
 */
function getAutoTheme() {
  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

/**
 * @param {string} theme
 * @return {void}
 */
function setTheme(theme) {
  document.documentElement.dataset.bsTheme =
    theme === "auto" ? getAutoTheme() : theme;

  const activeDropdown = themeSwitcher.querySelector(".dropdown-item.active");
  const activeDropdownIcon = activeDropdown.querySelector("i");

  const dropdownToActivate = themeSwitcher.querySelector(
    `[data-bs-theme-value="${theme}"]`
  );
  const dropdownToActivateIcon = dropdownToActivate.querySelector("i");

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

/**
 * @param {{readonly currentTarget: HTMLOrSVGElement}} e
 * @return {Promise<void>}
 */
function toggleHandler(e) {
  const theme = e.currentTarget.dataset.bsThemeValue;
  localStorage.setItem("theme", theme);
  setTheme(theme);
}

for (const toggle of themeSwitcher.querySelectorAll("[data-bs-theme-value]")) {
  toggle.addEventListener("click", toggleHandler);
}
