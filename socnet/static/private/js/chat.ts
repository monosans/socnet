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

const chatData = JSON.parse(document.querySelector("#data")!.textContent!) as {
  readonly interlocutorPk: number;
  readonly users: Record<string, User>;
};

function getSender(data: ChatMessageEvent): User {
  return chatData.users[data.sender.toLowerCase()];
}

const messageSendBtn =
  document.querySelector<HTMLButtonElement>("#messageSendBtn")!;

const messageTextarea =
  document.querySelector<HTMLTextAreaElement>("#id_content")!;

messageTextarea.addEventListener("keyup", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    messageSendBtn.click();
  }
});
messageTextarea.focus();

const chatLog = {
  element: document.querySelector("#chat-log")!,

  // eslint-disable-next-line sort-keys
  addNewMessage(data: ChatMessageEvent): void {
    const id = `msg${data.pk}`;
    const sender = getSender(data);
    const html = `
      <div id="${id}" class="d-flex mb-1">
        <a href="${sender.href}"
            class="avatar-thumbnail d-flex align-items-center me-2">
          ${
            sender.image
              ? `<img src="${sender.image}" loading="lazy" class="rounded" />`
              : '<i class="fa-solid fa-user text-secondary"></i>'
          }
        </a>
        <div>
          <a href="${sender.href}"
              class="link-underline link-underline-opacity-0 link-underline-opacity-100-hover text-break">${
                sender.displayName
              } <span class="text-secondary">@${data.sender}</span></a>
          <div class="text-secondary" data-epoch="${data.createdEpoch}">
          </div>
        </div>
      </div>
      <div class="markdown-container text-break">
        ${data.content}
      </div>
    `;
    this.element.insertAdjacentHTML("beforeend", html);
  },

  scrollToEnd(): void {
    this.element.scrollTop = this.element.scrollHeight;
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

const messageSendForm = document.querySelector("#messageSendForm")!;

messageSendForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const data = JSON.stringify({ message: messageTextarea.value });
  messageTextarea.value = "";
  messageTextarea.style.removeProperty("height");
  messageTextarea.focus();
  chatWs.send(data);
});
