interface User {
  href: string;
  image?: string;
  displayName: string;
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

const messageSendBtn = document.querySelector<HTMLElement>("#messageSendBtn")!;

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

  addNewMessage(data: ChatMessageEvent): void {
    const id = `msg${data.pk}`;
    const sender = chatData.users[data.sender.toLowerCase()]!;
    const html = `
      <div id="${id}" class="d-flex mb-1">
        <a href="${sender.href}"
            class="avatar-thumbnail d-flex align-items-center me-2">
          ${
            sender.image !== undefined
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

    void import("https://cdn.jsdelivr.net/npm/viewerjs@1/+esm").then(
      (viewer) => {
        new viewer.default(document.querySelector(id)!, { button: false });
      }
    );
  },

  scrollToEnd(): void {
    this.element.scrollTo(0, this.element.scrollHeight);
  },
};
chatLog.scrollToEnd();

const chatWs = ((): WebSocket => {
  const wsProtocol = window.location.protocol === "https:" ? "wss" : "ws";
  const ws = new WebSocket(
    `${wsProtocol}://${window.location.host}/ws/chat/${chatData.interlocutorPk}/`
  );
  ws.onmessage = (e: MessageEvent<string>): void => {
    // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
    const data: ChatMessageEvent = JSON.parse(e.data);

    chatLog.addNewMessage(data);
    chatLog.scrollToEnd();
  };
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
