document.addEventListener("DOMContentLoaded", function () {
  const chatBox = document.getElementById("chat-box");
  const chatForm = document.getElementById("chat-form");
  const userInput = document.getElementById("user-input");

  function appendMessage(sender, text) {
    const message = document.createElement("div");
    message.classList.add("message", sender === "user" ? "user-message" : "bot-message");
    message.textContent = text;
    chatBox.appendChild(message);
    scrollChatToBottom();
  }

  function showTypingIndicator() {
    const typingDiv = document.createElement("div");
    typingDiv.classList.add("typing-indicator");
    typingDiv.innerHTML = `
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
    `;
    typingDiv.id = "typing";
    chatBox.appendChild(typingDiv);
    scrollChatToBottom();
  }

  function removeTypingIndicator() {
    const typing = document.getElementById("typing");
    if (typing) typing.remove();
  }

  function scrollChatToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  async function sendMessage(message) {
    appendMessage("user", message);
    showTypingIndicator();
    try {
      const response = await fetch("https://bluejay-3999.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      const data = await response.json();
      removeTypingIndicator();
      appendMessage("bot", data.reply);
    } catch (error) {
      removeTypingIndicator();
      appendMessage("bot", "Oops! Something went wrong.");
    }
  }

  chatForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;
    userInput.value = "";
    sendMessage(message);
  });

  // Start conversation
  appendMessage("bot", "Hi, I'm BlueJay, your business expert. What's your name?");
});