document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("user-input").addEventListener("keypress", function (e) {
  if (e.key === "Enter") sendMessage();
});

function sendMessage() {
  const input = document.getElementById("user-input");
  const msg = input.value.trim();
  if (!msg) return;
  appendMessage("user", msg);
  input.value = "";

  showTyping(true);

  fetch("https://bluejay-3999.onrender.com/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: msg })
  })
  .then(res => res.json())
  .then(data => {
    showTyping(false);
    appendMessage("bot", data.reply);
  })
  .catch(() => {
    showTyping(false);
    appendMessage("bot", "Something went wrong.");
  });
}

function appendMessage(sender, text) {
  const chatlog = document.getElementById("chatlog");
  const bubble = document.createElement("div");
  bubble.className = sender === "user" ? "user-msg" : "bot-msg";
  bubble.innerText = text;
  chatlog.appendChild(bubble);
  chatlog.scrollTop = chatlog.scrollHeight;
}

function showTyping(show) {
  const el = document.getElementById("typing-indicator");
  el.classList.toggle("hidden", !show);
}