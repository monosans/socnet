import { requiredElement } from "../../dom";

function randomNumber(min: number, max: number): number {
  return Math.random() * (max - min) + min;
}

interface User {
  readonly href: string;
  readonly image?: string;
  readonly displayName: string;
  readonly isCurrentUser: boolean;
}

interface ChatMessageEvent {
  readonly pk: number;
  readonly content: string;
  readonly createdEpoch: number;
  readonly sender: string;
}

const chatData = JSON.parse(requiredElement("#data", HTMLElement).textContent) as {
  readonly interlocutorPk: number;
  readonly users: Record<string, User>;
};

function getSender(data: ChatMessageEvent): User {
  const sender = chatData.users[data.sender.toLowerCase()];
  if (!sender) {
    throw new Error(`The chat has no participant ${data.sender}`);
  }
  return sender;
}

function createElement<K extends keyof HTMLElementTagNameMap>(
  tag: K,
  className: string,
  ...children: readonly (Node | string)[]
): HTMLElementTagNameMap[K] {
  const element = document.createElement(tag);
  element.className = className;
  element.append(...children);
  return element;
}

const messageSendBtn = requiredElement("#messageSendBtn", HTMLButtonElement);

const messageTextarea = requiredElement("#id_content", HTMLTextAreaElement);

messageTextarea.addEventListener("keyup", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    messageSendBtn.click();
  }
});
messageTextarea.focus();

const chatLog = {
  addNewMessage(data: ChatMessageEvent): void {
    const sender = getSender(data);

    const avatar = createElement(
      "a",
      "avatar-thumbnail d-flex align-items-center me-2",
    );
    avatar.href = sender.href;
    if (sender.image) {
      const image = createElement("img", "rounded");
      image.src = sender.image;
      image.loading = "lazy";
      avatar.append(image);
    } else {
      avatar.append(createElement("i", "fa-solid fa-user text-secondary"));
    }

    const name = createElement(
      "a",
      "link-underline link-underline-opacity-0 link-underline-opacity-100-hover text-break",
    );
    name.href = sender.href;
    name.append(
      `${sender.displayName} `,
      createElement("span", "text-secondary", `@${data.sender}`),
    );
    const date = createElement("div", "text-secondary");
    date.dataset["epoch"] = data.createdEpoch.toString();

    const header = createElement("div", "d-flex mb-1");
    header.id = `msg${data.pk}`;
    header.append(avatar, createElement("div", "", name, date));

    // Markdown that the server rendered and sanitized.
    const content = createElement("div", "markdown-container text-break");
    content.innerHTML = data.content;

    chatLog.element.append(header, content);
  },

  element: requiredElement("#chat-log", HTMLElement),

  scrollToEnd(): void {
    chatLog.element.scrollTop = chatLog.element.scrollHeight;
  },
};
chatLog.scrollToEnd();

const chatWs = ((): WebSocket => {
  const wsProtocol = globalThis.location.protocol === "https:" ? "wss" : "ws";
  const ws = new WebSocket(
    `${wsProtocol}://${globalThis.location.host}/ws/chat/${chatData.interlocutorPk}/`,
  );
  ws.addEventListener("message", (e: MessageEvent<string>) => {
    const data = JSON.parse(e.data) as ChatMessageEvent;

    chatLog.addNewMessage(data);
    if (getSender(data).isCurrentUser) {
      chatLog.scrollToEnd();
    }
  });
  ws.addEventListener("close", (e) => {
    messageSendBtn.disabled = true;
    if (e.code === 1006 || e.code === 1011) {
      location.reload();
    } else if (e.code === 1012) {
      setTimeout(() => location.reload(), randomNumber(5000, 30_000));
    }
  });
  return ws;
})();

const messageSendForm = requiredElement("#messageSendForm", HTMLFormElement);

messageSendForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const data = JSON.stringify({ message: messageTextarea.value });
  messageTextarea.value = "";
  messageTextarea.style.removeProperty("height");
  messageTextarea.focus();
  chatWs.send(data);
});
