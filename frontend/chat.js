document.addEventListener("DOMContentLoaded", function () {
  const sendBtn = document.getElementById("send-btn");
  const userInput = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");

  // UUID setup
  function getOrCreateUUID() {
    let uuid = localStorage.getItem("bluejay_user_id");
    if (!uuid) {
      uuid = crypto.randomUUID();
      localStorage.setItem("bluejay_user_id", uuid);
    }
    return uuid;
  }

  function appendMessage(role, text) {
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

  async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    const user_id = getOrCreateUUID();
    appendMessage("user", message);
    userInput.value = "";
    userInput.disabled = true;
    sendBtn.disabled = true;

    appendMessage("assistant", "Thinking...");

    try {
      const response = await fetch("https://pbj-server1.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, user_id }),
        credentials: "include"
      });

      const data = await response.json();
      updateLastAssistantMessage(data.reply || "No response received.");
    } catch (err) {
      console.error("Chat error:", err);
      updateLastAssistantMessage("Oops! Something went wrong.");
    } finally {
      userInput.disabled = false;
      sendBtn.disabled = false;
      userInput.focus();
    }
  }

  sendBtn.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendMessage();
  });
});
