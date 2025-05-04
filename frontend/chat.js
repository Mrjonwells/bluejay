const chatBox = document.getElementById("chat-box");
const input = document.getElementById("chat-input");
const form = document.getElementById("chat-form");

function appendMessage(sender, text) {
  const bubble = document.createElement("div");
  bubble.className = `bubble ${sender}`;
  bubble.innerText = text;
  chatBox.appendChild(bubble);
  chatBox.scrollTop = chatBox.scrollHeight;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  appendMessage("user", message);
  input.value = "";

  appendMessage("assistant", "Typing...");

  try {
    const res = await fetch("https://bluejay-3999.onrender.com/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, user_id: "demo-user" }),
    });

    const data = await res.json();
    const lastBubble = chatBox.querySelector(".assistant:last-child");
    if (lastBubble) lastBubble.remove();
    appendMessage("assistant", data.response);
  } catch (err) {
    console.error(err);
    const lastBubble = chatBox.querySelector(".assistant:last-child");
    if (lastBubble) lastBubble.remove();
    appendMessage("assistant", "Something went wrong. Try again.");
  }
});