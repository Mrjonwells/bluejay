const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chatMessages = document.getElementById("chat-messages");

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const userMessage = chatInput.value.trim();
  if (!userMessage) return;

  appendMessage("You", userMessage);
  chatInput.value = "";

  appendMessage("BlueJay", "Thinking...");

  try {
    const response = await fetch("https://pbj-server1.onrender.com/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userMessage }),
    });

    const data = await response.json();
    chatMessages.lastChild.remove(); // remove "Thinking..."
    appendMessage("BlueJay", data.reply || "Hmm... I didn’t get that.");
  } catch (err) {
    chatMessages.lastChild.remove();
    appendMessage("BlueJay", "Something went wrong. Try again later.");
  }
});

function appendMessage(sender, text) {
  const msg = document.createElement("div");
  msg.innerHTML = `<strong>${sender}:</strong> ${text}`;
  chatMessages.appendChild(msg);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}