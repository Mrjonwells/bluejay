document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");
  const chatBox = document.getElementById("chat-box");

  function appendMessage(role, content) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${role}`;
    messageDiv.textContent = content;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    appendMessage("user", message);
    input.value = "";

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      const data = await response.json();
      appendMessage("assistant", data.reply);
    } catch (error) {
      appendMessage("assistant", "Error processing your message.");
    }
  }

  sendBtn.addEventListener("click", sendMessage);
  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });
});
