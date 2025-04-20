document.addEventListener("DOMContentLoaded", function () {
  const chatBox = document.getElementById("chat-box");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");

  // Send message on button click
  sendBtn.addEventListener("click", sendMessage);

  // Send message on Enter key press
  userInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  });

  function appendMessage(role, message) {
    const messageElem = document.createElement("div");
    messageElem.textContent = `${role}: ${message}`;
    chatBox.appendChild(messageElem);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage("You", message);
    userInput.value = "";

    try {
      const response = await fetch("/pbj", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();
      appendMessage("BlueJay", data.response || "There was an error.");
    } catch (error) {
      appendMessage("BlueJay", "Server error. Please try again later.");
      console.error("Chat error:", error);
    }
  }
});
