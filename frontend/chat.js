// chat.js

// Function to retrieve or generate a UUID for the user session
function getUserId() {
  let userId = localStorage.getItem("user_id");
  if (!userId) {
    userId = crypto.randomUUID();
    localStorage.setItem("user_id", userId);
  }
  return userId;
}

// Event listeners for sending messages
document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("user-input").addEventListener("keypress", function (e) {
  if (e.key === "Enter") sendMessage();
});

// Function to send the user's message to the server
function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  appendMessage("user", message);
  input.value = "";
  input.disabled = true;
  showThinking();

  fetch("https://pbj-server1.onrender.com/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      user_id: getUserId()
    }),
    credentials: "include"
  })
    .then(res => res.json())
    .then(data => {
      updateLastAssistantMessage(data.reply || "No response received.");
      input.disabled = false;
      input.focus();
    })
    .catch(err => {
      console.error("Chat error:", err);
      updateLastAssistantMessage("Oops! Something went wrong.");
      input.disabled = false;
      input.focus();
    });
}

// Function to append a message to the chat box
function appendMessage(role, text) {
  const chatBox = document.getElementById("chat-box");
  const msg = document.createElement("div");
  msg.className = `message ${role}`;
  msg.textContent = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Function to update the last assistant message
function updateLastAssistantMessage(newText) {
  const messages = document.querySelectorAll(".message.assistant");
  const last = messages[messages.length - 1];
  if (last) last.textContent = newText;
}

// Function to show a thinking indicator
function showThinking() {
  appendMessage("assistant", "Thinking...");
}
