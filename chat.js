document.addEventListener("DOMContentLoaded", function () {
  const sendBtn = document.getElementById("send-btn");
  const userInput = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");
  const thinkingIndicator = document.getElementById("thinking-indicator");

  function appendMessage(sender, text) {
    const message = document.createElement("div");
    message.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage("You", message);
    userInput.value = "";
    userInput.disabled = true;
    sendBtn.disabled = true;
    thinkingIndicator.style.display = "block";

    try {
      const response = await fetch("https://pbj-server1.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();
      appendMessage("BlueJay", data.response || "There was an error. Please try again.");
    } catch (err) {
      appendMessage("BlueJay", "There was an error reaching the server. Please try again later.");
    } finally {
      thinkingIndicator.style.display = "none";
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
