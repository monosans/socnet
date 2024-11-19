function getRequest(dataset: DOMStringMap): {
  url: string;
  options: RequestInit;
} {
  let body;
  let method;
  let url = "/api/subscriptions/";

  if (dataset["isSubscribed"] === "y") {
    url += `${dataset["username"]!}/`;
    method = "DELETE";
    body = null;
  } else {
    method = "POST";
    body = JSON.stringify({ username: dataset["username"] });
  }

  return {
    options: {
      body,
      headers: [
        ["Content-Type", "application/json"],
        [
          "X-CSRFToken",
          document.querySelector<HTMLInputElement>(
            '[name="csrfmiddlewaretoken"]',
          )!.value,
        ],
      ],
      method,
    },
    url,
  };
}

async function handler(e: Event): Promise<void> {
  const btn = (e.target as Element).closest<HTMLButtonElement>(
    "[data-is-subscribed]",
  );
  if (!btn) {
    return;
  }
  btn.disabled = true;

  const request = getRequest(btn.dataset);
  const response = await fetch(request.url, request.options);
  if (!response.ok) {
    throw new Error(
      `Subscribe API returned status ${response.status} (${response.statusText})`,
    );
  }

  const isSubscribe = request.options.method !== "DELETE";

  const subscribersCount =
    document.querySelector<HTMLElement>("#subscribersCount");

  if (subscribersCount) {
    const unformattedNumber = Number.parseInt(
      subscribersCount.dataset["unformattedNumber"]!,
    );
    subscribersCount.dataset["unformattedNumber"] = (
      unformattedNumber + (isSubscribe ? 1 : -1)
    ).toString();
  }

  btn.classList.toggle("btn-primary");
  btn.classList.toggle("btn-outline-primary");
  btn.dataset["isSubscribed"] = isSubscribe ? "y" : "n";
  [btn.textContent, btn.dataset["textToggle"]] = [
    btn.dataset["textToggle"]!,
    btn.textContent!,
  ];

  btn.disabled = false;
}

document.body.addEventListener("click", (e) => void handler(e));
