/**
 * @typedef {Object} User
 * @property {string} href
 * @property {string} [image]
 * @property {string} display_name
 */

/**
 * @typedef {Object} ChatMessageEvent
 * @property {number} pk
 * @property {string} content
 * @property {number} created_epoch
 * @property {string} sender
 */

/**
 * @type {{readonly interlocutorPk: number, readonly users: Object.<string, User>}}
 */
const chatData = JSON.parse(document.querySelector("#data").textContent);

/**
 * @type {HTMLElement}
 */
const messageSendBtn = document.querySelector("#messageSendBtn");

/**
 * @type {HTMLTextAreaElement}
 */
const messageTextarea = document.querySelector("#id_content");

messageTextarea.addEventListener("keyup", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    messageSendBtn.click();
  }
});
messageTextarea.focus();

const chatLog = {
  /**
   * @type {HTMLElement}
   */
  element: document.querySelector("#chat-log"),

  /**
   * @param {ChatMessageEvent} data
   * @return {void}
   */
  addNewMessage(data) {
    const id = `msg${data.pk}`;
    const sender = chatData.users[data.sender.toLowerCase()];
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
                sender.display_name
              } <span class="text-secondary">@${data.sender}</span></a>
          <div class="text-secondary" data-epoch="${data.created_epoch}">
          </div>
        </div>
      </div>
      <div class="markdown-container text-break">
        ${data.content}
      </div>
    `;
    this.element.insertAdjacentHTML("beforeend", html);

    void import("./viewer_gallery.mjs").then((createGallery) => {
      createGallery.default(document.querySelector(`#${id}`));
    });
  },

  /**
   * @return {void}
   */
  scrollToEnd() {
    this.element.scrollTo(0, this.element.scrollHeight);
  },
};
chatLog.scrollToEnd();

const chatWs = (() => {
  const wsProtocol = window.location.protocol === "https:" ? "wss" : "ws";
  const ws = new WebSocket(
    `${wsProtocol}://${window.location.host}/ws/chat/${chatData.interlocutorPk}/`
  );
  ws.onmessage = (e) => {
    /**
     * @type {ChatMessageEvent}
     */
    const data = JSON.parse(e.data);

    chatLog.addNewMessage(data);
    chatLog.scrollToEnd();
  };
  return ws;
})();

/**
 * @type {HTMLFormElement}
 */
const messageSendForm = document.querySelector("#messageSendForm");

messageSendForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const data = JSON.stringify({ message: messageTextarea.value });
  messageTextarea.value = "";
  messageTextarea.style.removeProperty("height");
  messageTextarea.focus();
  chatWs.send(data);
});
