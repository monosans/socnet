import { requiredElement } from "../../dom";

function randomNumber(min: number, max: number): number {
  return Math.random() * (max - min) + min;
}

interface ChatMessageEvent {
  readonly pk: number;
  readonly content: string;
  readonly createdEpoch: number;
  readonly sender: string;
}

const chatData = JSON.parse(
  requiredElement("#data", HTMLElement).textContent,
) as { readonly interlocutorPk: number };

/*
 * The header of a message from `sender`, which the template renders for each
 * participant, so that the data of a user never becomes markup here.
 */
function senderTemplate(sender: string): HTMLTemplateElement {
  return requiredElement(
    `#sender-${CSS.escape(sender.toLowerCase())}`,
    HTMLTemplateElement,
  );
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
    const header = document.importNode(
      senderTemplate(data.sender).content,
      true,
    );
    requiredElement("div", HTMLElement, header).id = `msg${data.pk}`;
    requiredElement("[data-epoch]", HTMLElement, header).dataset["epoch"] =
      data.createdEpoch.toString();

    // Markdown that the server rendered and sanitized.
    const content = document.createElement("div");
    content.className = "markdown-container text-break";
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
    if (Object.hasOwn(senderTemplate(data.sender).dataset, "currentUser")) {
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
