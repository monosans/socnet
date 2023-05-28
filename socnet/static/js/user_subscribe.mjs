import formatNumber from "./number_formatter.mjs";

/**
 * @param {DOMStringMap} dataset
 * @return {{url: string, options: RequestInit}}
 */
function getRequest(dataset) {
  /**
   * @type {string | null}
   */
  let body;

  /**
   * @type {string}
   */
  let method;

  /**
   * @type {string}
   */
  let url = "/api/subscriptions/";

  if (dataset.isSubscribed === "y") {
    url += `${dataset.username}/`;
    method = "DELETE";
    body = null;
  } else {
    method = "POST";
    body = JSON.stringify({ username: dataset.username });
  }

  /**
   * @type {HTMLInputElement}
   */
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]");

  return {
    options: {
      body,
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken.value,
      },
      method,
    },
    url,
  };
}
/**
 * @param {{readonly currentTarget: HTMLButtonElement}} e
 * @return {Promise<void>}
 */
async function handler(e) {
  const btn = e.currentTarget;
  btn.disabled = true;

  const request = getRequest(btn.dataset);
  const response = await fetch(request.url, request.options);
  if (!response.ok) {
    throw new Error(response);
  }

  const isSubscribe = request.options.method !== "DELETE";

  /**
   * @type {HTMLElement | null}
   */
  const subscribersCount = document.querySelector("#subscribersCount");

  if (subscribersCount) {
    const unformattedNumber = parseInt(
      subscribersCount.dataset.unformattedNumber
    );
    subscribersCount.dataset.unformattedNumber =
      unformattedNumber + (isSubscribe ? 1 : -1);
    formatNumber(subscribersCount);
  }

  btn.classList.toggle("btn-primary");
  btn.classList.toggle("btn-outline-primary");
  btn.dataset.isSubscribed = isSubscribe ? "y" : "n";
  [btn.textContent, btn.dataset.textToggle] = [
    btn.dataset.textToggle,
    btn.textContent,
  ];

  btn.disabled = false;
}

for (const btn of document.querySelectorAll("[data-is-subscribed]")) {
  btn.addEventListener("click", handler);
}
