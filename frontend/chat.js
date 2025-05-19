document.addEventListener("DOMContentLoaded", () => {
  const chatLog = document.getElementById("chatlog");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");

  const appendMessage = (sender, text) => {
    const msg = document.createElement("div");
    msg.className = sender === "user" ? "user-bubble" : "assistant-bubble";
    msg.textContent = text;
    chatLog.appendChild(msg);
    chatLog.scrollTop = chatLog.scrollHeight;
  };

  const sendMessage = async () => {
    const message = userInput.value.trim();
    if (!message) return;
    appendMessage("user", message);
    userInput.value = "";

    appendMessage("assistant", "Thinking...");

    try {
      const response = await fetch("https://bluejay-mjpg.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
      });

      const data = await response.json();
      const botMessage = data.reply || "Sorry, something went wrong.";
      chatLog.lastChild.remove();
      appendMessage("assistant", botMessage);
    } catch (err) {
      chatLog.lastChild.remove();
      appendMessage("assistant", "Error: Could not reach BlueJay.");
    }
  };

  sendBtn.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });
});
