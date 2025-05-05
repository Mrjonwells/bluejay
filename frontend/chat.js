document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("user-input").addEventListener("keypress", function (e) {
  if (e.key === "Enter") sendMessage();
});

window.onload = function () {
  appendMessage("bot", "Welcome to BlueJay, what’s your name?");
};

function sendMessage() {
  const inputField = document.getElementById("user-input");
  const message = inputField.value.trim();
  if (!message) return;

  appendMessage("user", message);
  inputField.value = "";

  const typing = document.createElement("div");
  typing.className = "bot-msg typing-indicator";
  typing.id = "typing";
  document.getElementById("chatlog").appendChild(typing);
  scrollChatToBottom();

  fetch("https://your-backend-url.com/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message }),
  })
    .then((res) => res.json())
    .then((data) => {
      const typingElem = document.getElementById("typing");
      if (typingElem) typingElem.remove();
      appendMessage("bot", data.reply);
    })
    .catch((err) => {
      console.error("Error:", err);
      const typingElem = document.getElementById("typing");
      if (typingElem) typingElem.remove();
      appendMessage("bot", "Something went wrong.");
    });
}

function appendMessage(sender, message) {
  const chatlog = document.getElementById("chatlog");
  const msg = document.createElement("div");
  msg.className = sender === "user" ? "user-msg" : "bot-msg";
  msg.innerText = message;
  chatlog.appendChild(msg);
  scrollChatToBottom();
}

function scrollChatToBottom() {
  const chatlog = document.getElementById("chatlog");
  chatlog.scrollTop = chatlog.scrollHeight;
}