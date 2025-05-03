const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  appendMessage("You", message);
  input.value = "";

  appendMessage("BlueJay", "Thinking...");

  try {
    const res = await fetch("https://your-render-backend-url.onrender.com/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    const data = await res.json();
    document.querySelectorAll(".assistant").slice(-1)[0].textContent = `BlueJay: ${data.reply}`;
  } catch (err) {
    document.querySelectorAll(".assistant").slice(-1)[0].textContent = "BlueJay: Sorry, something went wrong.";
  }
});

function appendMessage(sender, text) {
  const messageEl = document.createElement("div");
  messageEl.className = sender === "You" ? "user" : "assistant";
  messageEl.textContent = `${sender}: ${text}`;
  chatBox.appendChild(messageEl);
  chatBox.scrollTop = chatBox.scrollHeight;
}