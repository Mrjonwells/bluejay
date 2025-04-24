document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");

  sendBtn.addEventListener("click", sendMessage);
  input.addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendMessage();
  });

  function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    appendMessage("user", message);
    input.value = "";
    input.disabled = true;

    appendMessage("assistant", "Thinking...");

    fetch("https://pbj-server1.onrender.com/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
      credentials: "include"
    })
      .then((res) => res.json())
      .then((data) => {
        updateLastAssistantMessage(data.reply || "No response received.");
        input.disabled = false;
        input.focus();
      })
      .catch((err) => {
        console.error("Chat error:", err);
        updateLastAssistantMessage("Oops! Something went wrong.");
        input.disabled = false;
        input.focus();
      });
  }

  function appendMessage(role, text) {
    const chatBox = document.getElementById("chat-box");
    const msg = document.createElement("div");
    msg.className = `message ${role}`;
    msg.textContent = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function updateLastAssistantMessage(newText) {
    const messages = document.querySelectorAll(".message.assistant");
    const last = messages[messages.length - 1];
    if (last) last.textContent = newText;
  }
});