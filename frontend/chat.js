document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("user-input").addEventListener("keypress", function (e) {
  if (e.key === "Enter") sendMessage();
});

window.onload = () => {
  appendMessage("bot", "Welcome to BlueJay, what’s your name?");
};

function sendMessage() {
  const inputField = document.getElementById("user-input");
  const message = inputField.value.trim();
  if (!message) return;

  appendMessage("user", message);
  inputField.value = "";

  showTyping(true);

  fetch("https://bluejay-3999.onrender.com/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  })
    .then((res) => res.json())
    .then((data) => {
      showTyping(false);
      appendMessage("bot", data.reply || "Something went wrong.");
    })
    .catch(() => {
      showTyping(false);
      appendMessage("bot", "Something went wrong.");
    });
}

function appendMessage(sender, message) {
  const chatlog = document.getElementById("chatlog");
  const msg = document.createElement("div");
  msg.className = sender === "user" ? "user-msg" : "bot-msg";
  msg.textContent = message;
  chatlog.appendChild(msg);
  chatlog.scrollTop = chatlog.scrollHeight;
}

function showTyping(show) {
  const typingIndicator = document.getElementById("typing-indicator");
  typingIndicator.classList.toggle("hidden", !show);
  if (show) {
    const chatlog = document.getElementById("chatlog");
    chatlog.scrollTop = chatlog.scrollHeight;
  }
}
