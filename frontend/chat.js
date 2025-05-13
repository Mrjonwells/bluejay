document.addEventListener("DOMContentLoaded", () => {
  const sendBtn = document.getElementById("send-btn");
  const userInput = document.getElementById("user-input");
  const chatlog = document.getElementById("chatlog");

  function appendMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className = sender === "user" ? "user-msg" : "bot-msg";
    msg.innerText = text;
    chatlog.appendChild(msg);
    chatlog.scrollTop = chatlog.scrollHeight;
  }

  async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage(message, "user");
    userInput.value = "";

    try {
      const response = await fetch("https://bluejay-mjpg.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
      });

      const data = await response.json();

      if (data && data.reply) {
        appendMessage(data.reply, "bot");
      } else {
        appendMessage("Something went wrong.", "bot");
      }
    } catch (err) {
      appendMessage("Error connecting to server.", "bot");
    }
  }

  sendBtn.addEventListener("click", sendMessage);
  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
  });
});

function toggleMenu() {
  document.getElementById("dropdown").classList.toggle("hidden");
}