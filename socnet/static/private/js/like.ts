function getRequest(dataset: DOMStringMap): {
  url: string;
  options: RequestInit;
} {
  let url;
  if (dataset["postPk"]) {
    url = `/api/posts/${dataset["postPk"]}/likes`;
  } else if (dataset["commentPk"]) {
    url = `/api/comments/${dataset["commentPk"]}/likes`;
  } else {
    throw new Error(
      "Like button must contain data-post-pk or data-comment-pk attribute",
    );
  }

  return {
    options: {
      headers: [
        ["Content-Type", "application/json"],
        [
          "X-CSRFToken",
          document.querySelector<HTMLInputElement>(
            '[name="csrfmiddlewaretoken"]',
          )!.value,
        ],
      ],
      method: dataset["isLiked"] === "y" ? "DELETE" : "POST",
    },
    url,
  };
}

async function handler(e: Event): Promise<void> {
  const btn = (e.target as Element).closest<HTMLButtonElement>(
    "[data-is-liked]",
  );
  if (!btn) {
    return;
  }
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

  const iconClassList = btn.querySelector("i")!.classList;
  iconClassList.toggle("text-danger");
  iconClassList.toggle("fa-regular");
  iconClassList.toggle("fa-solid");

  btn.disabled = false;
}

document.body.addEventListener("click", (e) => void handler(e));
