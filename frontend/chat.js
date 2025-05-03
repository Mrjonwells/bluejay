document.addEventListener("DOMContentLoaded", function () {
  const chatContainer = document.getElementById("chat-container");
  const userInput = document.getElementById("user-input");
  const sendButton = document.getElementById("send-button");

  function appendMessage(text, isUser) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add(isUser ? "user-bubble" : "assistant-bubble");
    messageDiv.innerText = text;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  function showTypingIndicator() {
    const typing = document.createElement("div");
    typing.className = "assistant-bubble typing-indicator";
    typing.innerHTML =
      '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
    typing.id = "typing-indicator";
    chatContainer.appendChild(typing);
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  function removeTypingIndicator() {
    const typing = document.getElementById("typing-indicator");
    if (typing) typing.remove();
  }

  async function sendMessage() {
    const input = userInput.value.trim();
    if (!input) return;

    appendMessage(input, true);
    userInput.value = "";
    showTypingIndicator();

    try {
      const response = await fetch("https://askbluejay.ai/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();
      removeTypingIndicator();
      appendMessage(data.reply, false);
    } catch (error) {
      removeTypingIndicator();
      appendMessage("Something went wrong. Please try again.", false);
    }
  }

  sendButton.addEventListener("click", sendMessage);

  userInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  });

  // Start conversation
  appendMessage("Hi, I'm BlueJay — your business expert. What's your name?", false);
});