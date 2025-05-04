document.addEventListener("DOMContentLoaded", function () {
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");
  const chatMessages = document.getElementById("chat-messages");

  function appendMessage(sender, text) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", sender);
    messageElement.innerText = text;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  async function sendMessage(message) {
    appendMessage("user", message);
    chatInput.value = "";

    appendMessage("assistant", "...");
    const pending = chatMessages.lastChild;

    try {
      const response = await fetch("https://bluejay-3999.onrender.com/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: message,
          user_id: localStorage.getItem("bluejay_uid") || crypto.randomUUID(),
        }),
      });

      const data = await response.json();
      pending.remove();
      appendMessage("assistant", data.response);
    } catch (err) {
      pending.remove();
      appendMessage("assistant", "Error reaching the server.");
    }
  }

  chatForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (message) sendMessage(message);
  });
});
