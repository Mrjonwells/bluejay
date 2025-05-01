async function sendMessage() {
  const input = document.getElementById('userInput');
  const chatBox = document.getElementById('chatBox');
  const message = input.value.trim();
  if (!message) return;

  const userMsg = document.createElement('div');
  userMsg.textContent = message;
  userMsg.style.textAlign = 'right';
  chatBox.appendChild(userMsg);
  input.value = '';

  // Show "thinking" animation
  const thinkingMsg = document.createElement('div');
  thinkingMsg.textContent = 'BlueJay is thinking...';
  thinkingMsg.id = 'thinking';
  thinkingMsg.style.fontStyle = 'italic';
  thinkingMsg.style.opacity = 0.6;
  chatBox.appendChild(thinkingMsg);
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const response = await fetch('https://bluejay-3999.onrender.com/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, user_id: 'bluejay-user' })
    });

    const data = await response.json();

    // Remove thinking message
    const t = document.getElementById('thinking');
    if (t) t.remove();

    const botMsg = document.createElement('div');
    botMsg.textContent = data.reply || 'Sorry, something went wrong.';
    chatBox.appendChild(botMsg);
    chatBox.scrollTop = chatBox.scrollHeight;
  } catch (error) {
    const t = document.getElementById('thinking');
    if (t) t.remove();

    const errorMsg = document.createElement('div');
    errorMsg.textContent = 'Error: Unable to connect to the server.';
    chatBox.appendChild(errorMsg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }
}

// Listen for "Enter" key
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('userInput').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') sendMessage();
  });
});
