document.addEventListener("DOMContentLoaded", () => {
  const chatLog = document.getElementById("chatlog");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");

  function appendMessage(sender, message) {
    const msg = document.createElement("div");
    msg.className = sender === "user" ? "user-bubble" : "assistant-bubble";
    msg.innerText = message;
    chatLog.appendChild(msg);
    chatLog.scrollTop = chatLog.scrollHeight;
  }

  async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage("user", message);
    userInput.value = "";

    try {
      const response = await fetch("https://bluejay-mjpg.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
      });
      const data = await response.json();
      appendMessage("assistant", data.reply);
    } catch (err) {
      appendMessage("assistant", "Sorry, something went wrong.");
    }
  }

  sendBtn.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });
});
