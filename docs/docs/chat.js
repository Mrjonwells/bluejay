document.addEventListener("DOMContentLoaded", () => {
  const chatLog = document.getElementById("chatlog");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");

  function appendMessage(sender, text) {
    const msg = document.createElement("div");
    msg.className = sender === "user" ? "user-bubble" : "assistant-bubble";
    msg.textContent = text;
    chatLog.appendChild(msg);
    chatLog.scrollTop = chatLog.scrollHeight;
  }

  sendBtn.addEventListener("click", async () => {
    const message = userInput.value.trim();
    if (!message) return;
    appendMessage("user", message);
    userInput.value = "";

    try {
      const res = await fetch("https://bluejay-mjpg.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
      });
      const data = await res.json();
      appendMessage("assistant", data.reply);
    } catch (err) {
      appendMessage("assistant", "Something went wrong.");
    }
  });

  userInput.addEventListener("keydown", e => {
    if (e.key === "Enter") sendBtn.click();
  });
});
