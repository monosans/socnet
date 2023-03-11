"use strict";
(() => {
  /**
   * @param {EventTarget} btn
   * @return {{url: string, options: RequestInit}}
   */
  function getRequest(btn) {
    let url, value;
    if (btn.dataset.postPk) {
      url = "/api/post_like/";
      value = btn.dataset.postPk;
    } else if (btn.dataset.postCommentPk) {
      url = "/api/comment_like/";
      value = btn.dataset.postCommentPk;
    } else {
      throw new Error(
        "Button must contain data-post-pk or data-post-comment-pk attribute"
      );
    }

    let method, body;
    if (btn.dataset.isLiked === "y") {
      url += `${value}/`;
      method = "DELETE";
      body = null;
    } else {
      method = "POST";
      body = JSON.stringify({ pk: value });
    }

    return {
      url,
      options: {
        method,
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
            .value,
        },
        body,
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
      throw new Error(response);
    }

    const span = btn.querySelector("span");
    const likesCount = parseInt(span.textContent);
    if (btn.dataset.isLiked === "y") {
      span.textContent = likesCount - 1;
      btn.dataset.isLiked = "n";
    } else {
      span.textContent = likesCount + 1;
      btn.dataset.isLiked = "y";
    }

    const iconClassList = btn.querySelector("i").classList;
    iconClassList.toggle("text-danger");
    iconClassList.toggle("fa-regular");
    iconClassList.toggle("fa-solid");

    btn.disabled = false;
  }

  for (const btn of document.querySelectorAll("[data-is-liked]")) {
    btn.addEventListener("click", handler);
  }
})();
