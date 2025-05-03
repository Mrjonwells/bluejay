const messagesDiv = document.getElementById("chat-messages");
const userInput = document.getElementById("user-input");

function appendMessage(sender, text) {
  const msg = document.createElement("div");
  msg.className = sender;
  msg.textContent = text;
  messagesDiv.appendChild(msg);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function sendMessage() {
  const input = userInput.value.trim();
  if (!input) return;

  appendMessage("user", input);
  userInput.value = "";

  appendMessage("bot", "Thinking...");

  const response = await fetch("https://askbluejay.onrender.com/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: input, user_id: "browser-user" })
  });

  const data = await response.json();

  // Remove "Thinking..." and show actual reply
  const allMessages = messagesDiv.querySelectorAll(".bot");
  if (allMessages.length) {
    messagesDiv.removeChild(allMessages[allMessages.length - 1]);
  }

  appendMessage("bot", data.reply);
}

userInput.addEventListener("keypress", function (e) {
  if (e.key === "Enter") sendMessage();
});
