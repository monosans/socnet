import formatDates from "./date_formatter.js";

function randomNumber(min: number, max: number): number {
  return Math.random() * (max - min) + min;
}

interface User {
  href: string;
  image?: string;
  displayName: string;
  isCurrentUser: boolean;
}

interface ChatMessageEvent {
  pk: number;
  content: string;
  createdEpoch: number;
  sender: string;
}

// eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
const chatData: {
  interlocutorPk: number;
  users: Record<string, User>;
} = JSON.parse(document.querySelector("#data")!.textContent!);

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
  async addNewMessage(data: ChatMessageEvent): Promise<void> {
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

    const messageElement = document.querySelector<HTMLElement>(`#${id}`)!;
    await Promise.all([
      formatDates(messageElement),
      import("https://cdn.jsdelivr.net/npm/viewerjs@1/+esm").then(
        // eslint-disable-next-line @typescript-eslint/naming-convention
        ({ default: Viewer }) => {
          new Viewer(messageElement, { button: false });
        },
      ),
    ]);
  },

  scrollToEnd(): void {
    this.element.scrollTop = this.element.scrollHeight;
  },
};
chatLog.scrollToEnd();

const chatWs = ((): WebSocket => {
  const wsProtocol = window.location.protocol === "https:" ? "wss" : "ws";
  const ws = new WebSocket(
    `${wsProtocol}://${window.location.host}/ws/chat/${chatData.interlocutorPk}/`,
  );
  ws.addEventListener("message", (e: MessageEvent<string>) => {
    // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
    const data: ChatMessageEvent = JSON.parse(e.data);

    void chatLog.addNewMessage(data);
    if (getSender(data).isCurrentUser) {
      chatLog.scrollToEnd();
    }
  });
  ws.addEventListener("close", (e) => {
    messageSendBtn.disabled = true;
    if (e.code === 1006 || e.code === 1011) {
      location.reload();
    } else if (e.code === 1012) {
      setTimeout(() => location.reload(), randomNumber(5000, 30000));
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
