for (const button of document.querySelectorAll("[data-is-subscribed]")) {
  button.addEventListener("click", function () {
    let url = "/api/v1/subscription/",
      method,
      body;
    if (this.dataset.isSubscribed === "y") {
      method = "DELETE";
      body = null;
      url += `${this.dataset.userPk}/`;
    } else {
      method = "POST";
      body = JSON.stringify({ pk: this.dataset.userPk });
    }
    void fetch(url, {
      method: method,
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
          .value,
      },
      body: body,
    });
    for (const el of document.querySelectorAll(
      `[data-is-subscribed][data-user-pk="${this.dataset.userPk}"]`
    )) {
      el.classList.toggle("d-none");
    }
    const subscribers_count = document.querySelector(
      '[id="subscribers_count"]'
    );
    if (subscribers_count) {
      subscribers_count.innerHTML =
        parseInt(subscribers_count.innerHTML) + (method === "DELETE" ? -1 : 1);
    }
  });
}
