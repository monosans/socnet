import formatNumber from "./number_formatter.mjs";

/**
 * @param {DOMStringMap} dataset
 * @return {{url: string, options: RequestInit}}
 */
function getRequest(dataset) {
  /**
   * @type {string}
   */
  let value;

  /**
   * @type {string}
   */
  let url;

  if (dataset.postPk) {
    url = "/api/post-likes/";
    value = dataset.postPk;
  } else if (dataset.commentPk) {
    url = "/api/comment-likes/";
    value = dataset.commentPk;
  } else {
    throw new Error(
      "Like button must contain data-post-pk or data-comment-pk attribute"
    );
  }

  /**
   * @type {string | null}
   */
  let body;

  /**
   * @type {string}
   */
  let method;

  if (dataset.isLiked === "y") {
    url += `${value}/`;
    method = "DELETE";
    body = null;
  } else {
    method = "POST";
    body = JSON.stringify({ pk: value });
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

  /**
   * @type {HTMLSpanElement}
   */
  const span = btn.querySelector("span");

  const unformattedNumber = parseInt(span.dataset.unformattedNumber);
  if (btn.dataset.isLiked === "y") {
    btn.dataset.isLiked = "n";
    span.dataset.unformattedNumber = unformattedNumber - 1;
  } else {
    btn.dataset.isLiked = "y";
    span.dataset.unformattedNumber = unformattedNumber + 1;
  }
  formatNumber(span);

  const iconClassList = btn.querySelector("i").classList;
  iconClassList.toggle("text-danger");
  iconClassList.toggle("fa-regular");
  iconClassList.toggle("fa-solid");

  btn.disabled = false;
}

for (const btn of document.querySelectorAll("button[data-is-liked]")) {
  btn.addEventListener("click", handler);
}
