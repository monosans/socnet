"use strict";
(() => {
  const handler = (e) => {
    const btn = e.currentTarget;
    btn.setAttribute("disabled", "");
    let url, value;
    if (btn.dataset.postPk) {
      url = "/api/post_like/";
      value = btn.dataset.postPk;
    } else if (btn.dataset.postCommentPk) {
      url = "/api/post_comment_like/";
      value = btn.dataset.postCommentPk;
    } else {
      return;
    }
    const span = btn.querySelector("span");
    const likesCount = parseInt(span.innerHTML);
    let method, body;
    if (btn.dataset.isLiked === "y") {
      url += `${value}/`;
      method = "DELETE";
      body = null;
    } else {
      method = "POST";
      body = JSON.stringify({ pk: value });
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
      if (btn.dataset.isLiked === "y") {
        span.innerHTML = likesCount - 1;
        btn.dataset.isLiked = "n";
      } else {
        span.innerHTML = likesCount + 1;
        btn.dataset.isLiked = "y";
      }
      const iconClassList = btn.querySelector("i").classList;
      iconClassList.toggle("text-danger");
      iconClassList.toggle("fa-regular");
      iconClassList.toggle("fa-solid");
      btn.removeAttribute("disabled");
    });
  };
  for (const btn of document.querySelectorAll("[data-is-liked]")) {
    btn.addEventListener("click", handler);
  }
})();
