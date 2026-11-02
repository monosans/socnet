import { requiredData, requiredElement } from "../../dom";

const themeSwitcher = requiredElement("#themeSwitcher", HTMLElement);
const currentThemeIcon = requiredElement("#currentThemeIcon", HTMLElement);

function getStoredOrDefaultTheme(): "dark" | "light" {
  const storedTheme = localStorage.getItem("theme");
  if (storedTheme === "dark" || storedTheme === "light") {
    return storedTheme;
  }
  return globalThis.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function setTheme(): void {
  const theme = getStoredOrDefaultTheme();
  document.documentElement.dataset["bsTheme"] = theme;

  const activeDropdown = requiredElement(".dropdown-item.active", HTMLElement, themeSwitcher);
  const activeDropdownIcon = requiredElement("i", HTMLElement, activeDropdown);

  const dropdownToActivate = requiredElement(
    `[data-bs-theme-value="${CSS.escape(theme)}"]`,
    HTMLElement,
    themeSwitcher,
  );
  const dropdownToActivateIcon = requiredElement("i", HTMLElement, dropdownToActivate);

  activeDropdown.classList.remove("active");
  dropdownToActivate.classList.add("active");

  activeDropdownIcon.classList.add("text-primary");
  currentThemeIcon.className = dropdownToActivateIcon.className;
  dropdownToActivateIcon.classList.remove("text-primary");
}

setTheme();

globalThis.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", setTheme);

globalThis.addEventListener("storage", (e) => {
  if (e.key === "theme") {
    setTheme();
  }
});

document.body.addEventListener("click", (e) => {
  const btn = (e.target as Element).closest<HTMLElement>("[data-bs-theme-value]");
  if (!btn) {
    return;
  }
  const theme = requiredData(btn, "bsThemeValue");
  localStorage.setItem("theme", theme);
  setTheme();
});
