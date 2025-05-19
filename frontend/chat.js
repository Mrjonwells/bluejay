document.addEventListener("DOMContentLoaded", () => {
  const chatLog = document.getElementById("chatlog");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");
  const menuIcon = document.querySelector(".menu-icon");
  const dropdownMenu = document.querySelector(".dropdown-menu");

  // Toggle dropdown menu
  menuIcon.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });

  // Send message handler
  function appendMessage(sender, text) {
    const message = document.createElement("div");
    message.className = sender === "user" ? "user-bubble" : "assistant-bubble";
    message.innerText = text;
    chatLog.appendChild(message);
    chatLog.scrollTop = chatLog.scrollHeight;
  }

  async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    appendMessage("user", message);
    userInput.value = "";

    appendMessage("assistant", "BlueJay is typing...");

    const response = await fetch("https://bluejay-mjpg.onrender.com/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    const data = await response.json();
    chatLog.lastChild.remove(); // Remove "typing..."
    appendMessage("assistant", data.reply);
  }

  sendBtn.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });
});
