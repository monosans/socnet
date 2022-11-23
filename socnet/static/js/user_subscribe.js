"use strict";
(() => {
  function handler(e) {
    const btn = e.currentTarget;
    btn.setAttribute("disabled", "");
    let url = "/api/subscription/",
      method,
      body;
    if (btn.dataset.isSubscribed === "y") {
      url += `${btn.dataset.userPk}/`;
      method = "DELETE";
      body = null;
    } else {
      method = "POST";
      body = JSON.stringify({ pk: btn.dataset.userPk });
    }
    void fetch(url, {
      method: method,
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
          .value,
      },
      body: body,
    }).then((value) => {
      if (!value.ok) {
        return;
      }
      for (const el of document.querySelectorAll(
        `[data-is-subscribed][data-user-pk="${btn.dataset.userPk}"]`
      )) {
        el.classList.toggle("d-none");
      }
      const subscribers_count = document.querySelector(
        '[id="subscribers_count"]'
      );
      if (subscribers_count) {
        subscribers_count.innerHTML =
          parseInt(subscribers_count.innerHTML) +
          (method === "DELETE" ? -1 : 1);
      }
      btn.removeAttribute("disabled");
    });
  };
  for (const btn of document.querySelectorAll("[data-is-subscribed]")) {
    btn.addEventListener("click", handler);
  }
})();
