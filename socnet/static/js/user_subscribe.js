"use strict";
(() => {
  /**
   * @param {EventTarget} btn
   * @return {{url: string, options: RequestInit}}
   */
  function getRequest(btn) {
    let url = "/api/subscription/",
      method,
      body;
    if (btn.dataset.isSubscribed === "y") {
      url += `${btn.dataset.username}/`;
      method = "DELETE";
      body = null;
    } else {
      method = "POST";
      body = JSON.stringify({ username: btn.dataset.username });
    }
    return {
      url: url,
      options: {
        method: method,
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
            .value,
        },
        body: body,
      },
    };
  }

  /**
   * @param {Event} e
   * @return {Promise<void>}
   */
  async function handler(e) {
    const btn = e.currentTarget;
    btn.disabled = true;

    const request = getRequest(btn);
    const response = await fetch(request.url, request.options);
    if (!response.ok) {
      Promise.reject(new Error(response));
      return;
    }

    const subscribersCount = document.querySelector('[id="subscribers_count"]');
    if (subscribersCount) {
      subscribersCount.textContent =
        parseInt(subscribersCount.textContent) +
        (request.options.method === "DELETE" ? -1 : 1);
    }

    const username = btn.dataset.username;
    const subBtns = document.querySelectorAll(
      `[data-is-subscribed][data-username="${username}"]`
    );
    for (const subBtn of subBtns) {
      subBtn.classList.toggle("d-none");
    }

    btn.disabled = false;
  }

  for (const btn of document.querySelectorAll("[data-is-subscribed]")) {
    btn.addEventListener("click", handler);
  }
})();
