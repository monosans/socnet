"use strict";
(() => {
  const themeSwitcher = document.querySelector("#themeSwitcher");
  const currentThemeIcon = themeSwitcher.querySelector("#currentThemeIcon");

  /**
   * @return {void}
   */
  function getTheme() {
    const storedTheme = localStorage.getItem("theme");
    if (["light", "dark", "auto"].includes(storedTheme)) {
      return storedTheme;
    }

    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  /**
   * @param {string} theme
   * @return {void}
   */
  function setTheme(theme) {
    const themeAttribute =
      theme === "auto" &&
      window.matchMedia("(prefers-color-scheme: dark)").matches
        ? "dark"
        : theme;
    document.documentElement.dataset.bsTheme = themeAttribute;

    const activeDropdownTheme = themeSwitcher.querySelector(
      ".dropdown-item.active"
    );
    const dropdownThemeToActivate = themeSwitcher.querySelector(
      `[data-bs-theme-value="${theme}"]`
    );
    const dropdownToActivateIcon = dropdownThemeToActivate.querySelector("i");

    activeDropdownTheme.classList.remove("active");
    dropdownThemeToActivate.classList.add("active");

    activeDropdownTheme.querySelector("i").classList.add("text-primary");
    currentThemeIcon.className = dropdownToActivateIcon.className;
    dropdownToActivateIcon.classList.remove("text-primary");
  }

  setTheme(getTheme());
  window
    .matchMedia("(prefers-color-scheme: dark)")
    .addEventListener("change", () => setTheme(getTheme()));

  for (const toggle of themeSwitcher.querySelectorAll(
    "[data-bs-theme-value]"
  )) {
    toggle.addEventListener("click", (e) => {
      const theme = e.currentTarget.dataset.bsThemeValue;
      localStorage.setItem("theme", theme);
      setTheme(theme);
    });
  }
})();
