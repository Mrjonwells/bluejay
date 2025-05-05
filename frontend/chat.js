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

  fetch("https://bluejay-3999.onrender.com/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  })
    .then((res) => res.json())
    .then((data) => appendMessage("bot", data.reply || "Something went wrong."))
    .catch(() => appendMessage("bot", "Something went wrong."));
}

function appendMessage(sender, message) {
  const chatlog = document.getElementById("chatlog");
  const msg = document.createElement("div");
  msg.className = sender === "user" ? "user-msg" : "bot-msg";
  msg.innerText = message;
  chatlog.appendChild(msg);
  chatlog.scrollTop = chatlog.scrollHeight;
}