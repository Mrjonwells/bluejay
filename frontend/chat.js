document.addEventListener("DOMContentLoaded", () => {
  const chatLog = document.getElementById("chatlog");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");

  const appendMessage = (sender, text) => {
    const bubble = document.createElement("div");
    bubble.className = sender === "user" ? "user-bubble" : "bot-bubble";
    bubble.innerText = text;
    chatLog.appendChild(bubble);
    chatLog.scrollTop = chatLog.scrollHeight;
  };

  const sendMessage = async () => {
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage("user", message);
    userInput.value = "";

    try {
      const response = await fetch("https://bluejay-mjpg.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();
      appendMessage("bot", data.reply || "Something went wrong.");
    } catch (err) {
      appendMessage("bot", "Error: couldn't reach server.");
    }
  };

  sendBtn.addEventListener("click", sendMessage);
  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
  });
});
