const form = document.getElementById("chat-form");
const input = document.getElementById("chat-input");
const chatBox = document.getElementById("chat-messages");

let user_id = localStorage.getItem("user_id");
if (!user_id) {
  user_id = crypto.randomUUID();
  localStorage.setItem("user_id", user_id);
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  appendMessage("You", message);
  input.value = "";

  appendMessage("BlueJay", "...");
  const response = await fetch("https://pbj-server1.onrender.com/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, user_id })
  });

  const data = await response.json();
  removeLastMessageIfDots();
  appendMessage("BlueJay", data.reply);
});

function appendMessage(sender, text) {
  const div = document.createElement("div");
  div.innerHTML = `<strong>${sender}:</strong> ${text}`;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function removeLastMessageIfDots() {
  const last = chatBox.lastChild;
  if (last && last.textContent.includes("...")) {
    chatBox.removeChild(last);
  }
}