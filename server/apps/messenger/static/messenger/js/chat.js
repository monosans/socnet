"use strict";
(() => {
  const chatPk = JSON.parse(document.getElementById("chat-pk").textContent);
  const chatLog = document.getElementById("chat-log");
  const textarea = document.getElementById("id_text");
  const submitBtn = document.getElementById("chat-message-submit");
  chatLog.scrollTo(0, chatLog.scrollHeight);
  const proto = window.location.protocol === "https:" ? "wss" : "ws";
  const chatSocket = new WebSocket(
    `${proto}://${window.location.host}/ws/chat/${chatPk}/`
  );
  chatSocket.onmessage = (e) => {
    const data = JSON.parse(e.data);
    let text = "";
    for (const [index, line] of data.text.split(/\r?\n/).entries()) {
      if (index !== 0) {
        text += "<br/>";
      }
      text += line;
    }
    let html = '<div class="row mb-3"><div class="avatar-thumbnail">';
    if (data.user__image) {
      html += `<img src="${data.user__image}" alt="" class="rounded" loading="lazy"/>`;
    }
    html += `</div><div class="col ms-2"><div class="text-break"><div><a href="${data.user_href}">${data.user__username}</a> <span class="text-secondary">${data.date}</span></div><div class="me-2">${text}</div></div></div></div>`;
    chatLog.innerHTML += html;
    chatLog.scrollTo(0, chatLog.scrollHeight);
  };
  submitBtn.addEventListener("click", () => {
    chatSocket.send(
      JSON.stringify({
        message: textarea.value,
      })
    );
    textarea.value = "";
  });
  textarea.addEventListener("keyup", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      submitBtn.click();
    }
  });
  textarea.focus();
})();
