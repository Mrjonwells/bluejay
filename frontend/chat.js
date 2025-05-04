const chatBox = document.getElementById("chat-box");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const typingIndicator = document.getElementById("typing-indicator");

function appendMessage(role, message) {
  const bubble = document.createElement("div");
  bubble.classList.add("bubble", role);
  bubble.textContent = message;
  chatBox.appendChild(bubble);
  chatBox.scrollTop = chatBox.scrollHeight;
}

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = chatInput.value.trim();
  if (!message) return;

  appendMessage("user", message);
  chatInput.value = "";
  typingIndicator.classList.remove("hidden");

  try {
    const res = await fetch("https://bluejay-api.onrender.com/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });
    const data = await res.json();
    appendMessage("assistant", data.response);
  } catch (err) {
    appendMessage("assistant", "Something went wrong.");
  }

  typingIndicator.classList.add("hidden");
});