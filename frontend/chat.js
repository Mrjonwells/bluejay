document.addEventListener("DOMContentLoaded", function () {
  const sendBtn = document.getElementById("send-btn");
  const userInput = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");
  const thinkingIcon = document.getElementById("thinking");

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

    appendMessage("user", message);
    userInput.value = "";
    userInput.disabled = true;
    sendBtn.disabled = true;
    thinkingIcon.style.display = "inline-block";

    appendMessage("assistant", "Thinking...");

    try {
      const res = await fetch("https://pbj-server1.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
        credentials: "include"
      });

      const data = await res.json();
      updateLastAssistantMessage(data.reply || "No response received.");
    } catch (err) {
      console.error("Chat error:", err);
      updateLastAssistantMessage("Oops! Something went wrong.");
    } finally {
      userInput.disabled = false;
      sendBtn.disabled = false;
      thinkingIcon.style.display = "none";
      userInput.focus();
    }
  }

  sendBtn.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendMessage();
  });
});