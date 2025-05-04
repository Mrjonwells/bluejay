document.addEventListener("DOMContentLoaded", function () {
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");
  const chatContainer = document.getElementById("chat-container");
  const typingIndicator = document.getElementById("typing-indicator");
  const userId = localStorage.getItem("bluejay_user_id") || crypto.randomUUID();
  localStorage.setItem("bluejay_user_id", userId);

  function addMessage(message, sender) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", sender);
    messageElement.textContent = message;
    chatContainer.appendChild(messageElement);
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  function showTyping(show) {
    typingIndicator.style.display = show ? "block" : "none";
  }

  chatForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (!message) return;

    addMessage(message, "user");
    chatInput.value = "";
    showTyping(true);

    try {
      const response = await fetch("https://bluejay-3999.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, user_id: userId })
      });

      const data = await response.json();
      if (data.response) {
        addMessage(data.response, "assistant");
      } else {
        addMessage("Hmm... no reply came back.", "assistant");
      }
    } catch (error) {
      addMessage("Error talking to BlueJay. Try again.", "assistant");
    } finally {
      showTyping(false);
    }
  });
});
