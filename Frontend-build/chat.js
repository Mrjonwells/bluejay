const API_BASE = "https://pbj-server1.onrender.com";

function appendMessage(content, type) {
  const chatBox = document.getElementById("chat-box");
  const msg = document.createElement("div");
  msg.className = `message ${type}-message`;
  msg.innerText = content;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  appendMessage(message, "user");
  input.value = "";

  try {
    const res = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    const data = await res.json();
    appendMessage(data.reply, "bot");

    if (["done", "submit", "that's all"].includes(message.toLowerCase())) {
      await fetch(`${API_BASE}/submit-to-hubspot`, { method: "POST" });
      appendMessage("Thanks! I’ve submitted your info.", "bot");
    }
  } catch (err) {
    console.error("Chat error:", err);
    appendMessage("Oops! Something went wrong. Please try again.", "bot");
  }
}
