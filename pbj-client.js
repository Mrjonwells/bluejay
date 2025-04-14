const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('userInput');
const submitBtn = document.getElementById('submitBtn');

// Wakes up the Render server on first page load
(async function warmUpServer() {
  await fetch("https://pbj-server1.onrender.com/");
})();

function addMessage(text, role) {
  const bubble = document.createElement('div');
  bubble.className = `bubble ${role}`;
  bubble.textContent = text;
  chatContainer.appendChild(bubble);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function addThinkingBubble() {
  const loadingBubble = document.createElement('div');
  loadingBubble.className = 'bubble bot';
  loadingBubble.innerHTML = `<span class="dots">BlueJay is thinking<span class="dot one">.</span><span class="dot two">.</span><span class="dot three">.</span></span>`;
  chatContainer.appendChild(loadingBubble);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  addMessage(message, 'user');
  userInput.value = '';

  addThinkingBubble();

  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15000); // safety timeout

    const res = await fetch("https://pbj-server1.onrender.com/pbj", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
      signal: controller.signal
    });

    clearTimeout(timeout);

    const data = await res.json();

    // Remove the "thinking" message
    const last = document.querySelector('.bot:last-child');
    if (last && last.innerHTML.includes("BlueJay is thinking")) {
      last.remove();
    }

    addMessage(data.response || "No response received.", 'bot');
  } catch (err) {
    const last = document.querySelector('.bot:last-child');
    if (last && last.innerHTML.includes("BlueJay is thinking")) {
      last.remove();
    }

    addMessage("Sorry, something went wrong. Try again in a moment.", 'bot');
  }
}

// Click send button
submitBtn.addEventListener('click', sendMessage);

// Press Enter key
userInput.addEventListener('keydown', function (e) {
  if (e.key === 'Enter') {
    e.preventDefault(); // prevent newline
    sendMessage();
  }
});
