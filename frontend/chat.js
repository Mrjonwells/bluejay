// frontend/chat.js

function getUserId() {
  let userId = localStorage.getItem("bluejay_user_id");
  if (!userId) {
    userId = crypto.randomUUID();
    localStorage.setItem("bluejay_user_id", userId);
  }
  return userId;
}

document.getElementById("chat-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const input = document.getElementById("chat-input");
  const message = input.value.trim();
  if (!message) return;

  const userId = getUserId();
  appendMessage("user", message);

  input.value = "";
  showThinking();

  const response = await fetch("https://pbj-server1.onrender.com/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, user_id: userId })
  });

  const data = await response.json();
  hideThinking();
  appendMessage("assistant", data.reply);
});
