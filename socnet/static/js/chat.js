"use strict";
(() => {
  const chatPk = JSON.parse(document.getElementById("chat-pk").textContent);
  const chatLog = document.getElementById("chat-log");
  const textarea = document.getElementById("id_text");
  const submitBtn = document.getElementById("messageSubmitBtn");
  const form = document.getElementById("messageSendForm");
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
    if (data.user.image) {
      html += `<img src="${data.user.image}" alt="" class="rounded" loading="lazy"/>`;
    }
    html += `</div><div class="col ms-2"><div class="text-break"><div><a href="${data.user.href}" class="text-decoration-none">${data.user.username}</a> <span class="text-secondary">${data.date}</span></div><div class="me-2">${text}</div></div></div></div>`;
    chatLog.innerHTML += html;
    chatLog.scrollTo(0, chatLog.scrollHeight);
  };
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    chatSocket.send(
      JSON.stringify({
        message: textarea.value,
      })
    );
    textarea.value = "";
    textarea.focus();
  });
  textarea.addEventListener("input", () => {
    if (/^\s+$/.test(textarea.value)) {
      textarea.value = "";
    }
  });
  textarea.addEventListener("keyup", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      submitBtn.click();
    }
  });
  textarea.focus();
})();
