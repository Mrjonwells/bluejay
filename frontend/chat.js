document.addEventListener("DOMContentLoaded", function () {
  const sendButton = document.getElementById("send-button");
  const userInput = document.getElementById("user-input");
  const chatContainer = document.getElementById("chat-container");
  const typingIndicator = document.getElementById("typing-indicator");

  function appendMessage(content, sender) {
    const msg = document.createElement("div");
    msg.className = `message ${sender}`;
    msg.innerText = content;
    chatContainer.appendChild(msg);
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  function showTyping(show) {
    typingIndicator.style.display = show ? "flex" : "none";
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage(message, "user");
    userInput.value = "";

    showTyping(true);

    try {
      const response = await fetch("https://bluejay-3999.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
      });

      const data = await response.json();
      showTyping(false);

      if (data && data.response) {
        appendMessage(data.response, "bot");
      } else {
        appendMessage("Hmm... no reply received.", "bot");
      }
    } catch (error) {
      showTyping(false);
      appendMessage("Oops! Something went wrong.", "bot");
    }
  }

  sendButton.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendMessage();
  });
});
