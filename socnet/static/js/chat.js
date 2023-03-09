"use strict";
(() => {
  class ChatLog {
    /**
     * @param {string} id
     */
    constructor(id) {
      this.element = document.querySelector(`#${id}`);
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
        <div class="row mb-3" id="message${data.pk}">
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
                ${data.date_created}
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
    const interlocutor_pk =
      document.querySelector("#interlocutor_pk").textContent;
    const wsProtocol = window.location.protocol === "https:" ? "wss" : "ws";
    return new WebSocket(
      `${wsProtocol}://${window.location.host}/ws/chat/${interlocutor_pk}/`
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

  const messageTextarea = document.querySelector("#id_content");

  const messageSendBtn = document.querySelector("#messageSendBtn");
  messageTextarea.addEventListener("keyup", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      messageTextarea.style.removeProperty("height");
      messageSendBtn.click();
    }
  });

  document.querySelector("#messageSendForm").addEventListener("submit", (e) => {
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
