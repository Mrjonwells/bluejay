document.addEventListener("DOMContentLoaded", function () {
  const sendButton = document.getElementById("send-button");
  const userInput = document.getElementById("user-input");
  const chatContainer = document.getElementById("chat-container");
  const thinkingIcon = document.getElementById("thinking-icon");

  function appendMessage(content, sender) {
    const message = document.createElement("div");
    message.className = `message ${sender}`;
    message.textContent = content;
    chatContainer.appendChild(message);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return message;
  }

  async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    appendMessage(text, "user");
    userInput.value = "";

    thinkingIcon.style.display = "inline";
    const typing = appendMessage("BlueJay is typing...", "bot");
    typing.classList.add("typing");

    try {
      const response = await fetch("https://bluejay-3999.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });

      const data = await response.json();

      if (data && data.response) {
        typing.remove(); // Remove 'typing' placeholder
        appendMessage(data.response, "bot");
      } else {
        typing.textContent = "Sorry, I didn’t get a reply.";
      }
    } catch (error) {
      typing.textContent = "Oops! Something went wrong.";
    } finally {
      thinkingIcon.style.display = "none";
    }
  }

  sendButton.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendMessage();
  });
});
