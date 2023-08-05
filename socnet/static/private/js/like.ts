import formatNumber from "./number_formatter.js";

function getRequest(dataset: DOMStringMap): {
  url: string;
  options: RequestInit;
} {
  let value;
  let url;

  if (dataset["postPk"]) {
    url = "/api/post-likes/";
    value = dataset["postPk"];
  } else if (dataset["commentPk"]) {
    url = "/api/comment-likes/";
    value = dataset["commentPk"];
  } else {
    throw new Error(
      "Like button must contain data-post-pk or data-comment-pk attribute",
    );
  }

  let body;
  let method;
  if (dataset["isLiked"] === "y") {
    url += `${value}/`;
    method = "DELETE";
    body = null;
  } else {
    method = "POST";
    body = JSON.stringify({ pk: value });
  }

  return {
    options: {
      body,
      headers: [
        ["Content-Type", "application/json"],
        [
          "X-CSRFToken",
          document.querySelector<HTMLInputElement>(
            "[name=csrfmiddlewaretoken]",
          )!.value,
        ],
      ],
      method,
    },
    url,
  };
}

async function handler(e: Event): Promise<void> {
  const btn = e.currentTarget! as HTMLButtonElement;
  btn.disabled = true;

  const request = getRequest(btn.dataset);
  const response = await fetch(request.url, request.options);
  if (!response.ok) {
    throw new Error(
      `Like API returned status ${response.status} (${response.statusText})`,
    );
  }

  const span = btn.querySelector("span")!;

  const unformattedNumber = Number.parseInt(span.dataset["unformattedNumber"]!);
  if (btn.dataset["isLiked"] === "y") {
    btn.dataset["isLiked"] = "n";
    span.dataset["unformattedNumber"] = (unformattedNumber - 1).toString();
  } else {
    btn.dataset["isLiked"] = "y";
    span.dataset["unformattedNumber"] = (unformattedNumber + 1).toString();
  }
  formatNumber(span);

  const iconClassList = btn.querySelector("i")!.classList;
  iconClassList.toggle("text-danger");
  iconClassList.toggle("fa-regular");
  iconClassList.toggle("fa-solid");

  btn.disabled = false;
}

for (const btn of document.querySelectorAll<HTMLButtonElement>(
  "[data-is-liked]",
)) {
  btn.addEventListener("click", (e) => void handler(e));
}
