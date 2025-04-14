const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('userInput');
const submitBtn = document.getElementById('submitBtn');

function addMessage(text, role) {
  const bubble = document.createElement('div');
  bubble.className = `bubble ${role}`;
  bubble.textContent = text;
  chatContainer.appendChild(bubble);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

submitBtn.addEventListener('click', async () => {
  const message = userInput.value.trim();
  if (!message) return;

  addMessage(message, 'user');
  userInput.value = '';

  addMessage("PBJ is thinking...", 'bot');

  try {
    const res = await fetch("https://pbj-server1.onrender.com/pbj", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    const data = await res.json();
    // Remove the loading placeholder
    const last = document.querySelector('.bot:last-child');
    if (last && last.textContent === "PBJ is thinking...") {
      last.remove();
    }

    addMessage(data.response || "No response received.", 'bot');
  } catch (err) {
    addMessage("Something went wrong. Try again.", 'bot');
  }
});
