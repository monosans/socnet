"use strict";
(() => {
  class ChatLog {
    /**
     * @param {string} id
     */
    constructor(id) {
      this.element = document.getElementById(id);
    }

    /**
     * @return {void}
     */
    scrollToEnd() {
      this.element.scrollTo(0, this.element.scrollHeight);
    }

    /**
     * @param {any} data
     * @return {void}
     */
    addNewMessage(data) {
      const html = `
<div class="row mb-3" id="${data.pk}">
  <div class="avatar-thumbnail">
    ${
      data.sender.image
        ? `<img
             src="${data.sender.image}"
             alt=""
             class="rounded"
             loading="lazy"
           />`
        : ""
    }
  </div>
  <div class="col ms-2">
    <div class="text-break">
      <div>
        <a href="${data.sender.href}" class="text-decoration-none">
          ${data.sender.username} ${data.sender.display_name}
        </a>
        <a href="${data.href}" class="text-decoration-none text-secondary">
          ${data.date_created}
        </a>
      </div>
      <div class="me-2 img-responsive">${data.content}</div>
    </div>
  </div>
</div>
`;
      this.element.insertAdjacentHTML("beforeend", html);
    }
  }

  const chatLog = new ChatLog("chat-log");
  chatLog.scrollToEnd();

  /**
   * @return {WebSocket}
   */
  function createChatWebSocket() {
    const chatPk = document.getElementById("chat_pk").textContent;
    const wsProtocol = window.location.protocol === "https:" ? "wss" : "ws";
    return new WebSocket(
      `${wsProtocol}://${window.location.host}/ws/chat/${chatPk}/`
    );
  }

  /**
   * @param {WebSocket} ws
   * @return {void}
   */
  function registerOnMessageHandler(ws) {
    ws.onmessage = (e) => {
      const data = JSON.parse(e.data);
      chatLog.addNewMessage(data);
      chatLog.scrollToEnd();
    };
  }

  const chatWs = createChatWebSocket();
  registerOnMessageHandler(chatWs);

  const messageTextarea = document.getElementById("id_content");

  const messageSendBtn = document.getElementById("messageSendBtn");
  messageTextarea.addEventListener("keyup", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      messageTextarea.style.removeProperty("height");
      messageSendBtn.click();
    }
  });

  document.getElementById("messageSendForm").addEventListener("submit", (e) => {
    e.preventDefault();
    const data = JSON.stringify({
      message: messageTextarea.value,
    });
    messageTextarea.value = "";
    messageTextarea.focus();
    chatWs.send(data);
  });

  messageTextarea.focus();
})();
