"use strict";
(() => {
  for (const button of document.querySelectorAll("[data-is-liked]")) {
    button.addEventListener("click", function () {
      let url, value;
      if (this.dataset.postPk) {
        url = "/api/post_like/";
        value = this.dataset.postPk;
      } else if (this.dataset.postCommentPk) {
        url = "/api/post_comment_like/";
        value = this.dataset.postCommentPk;
      } else {
        return;
      }
      const csrfToken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
      ).value;
      const span = this.querySelector("span");
      const likesCount = parseInt(span.innerHTML);
      let method, body;
      if (this.dataset.isLiked === "y") {
        url += `${value}/`;
        method = "DELETE";
        body = null;
        this.dataset.isLiked = "n";
        span.innerHTML = likesCount - 1;
      } else {
        method = "POST";
        body = JSON.stringify({ pk: value });
        this.dataset.isLiked = "y";
        span.innerHTML = likesCount + 1;
      }
      void fetch(url, {
        method: method,
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: body,
      });
      const iconClassList = this.querySelector("i").classList;
      iconClassList.toggle("text-danger");
      iconClassList.toggle("fa-regular");
      iconClassList.toggle("fa-solid");
    });
  }
})();
