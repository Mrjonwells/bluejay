// chat.js
async function sendMessage() {
  const input = document.getElementById('userInput');
  const chatBox = document.getElementById('chatBox');
  const message = input.value.trim();
  if (!message) return;

  // Append user message
  const userMsg = document.createElement('div');
  userMsg.textContent = message;
  userMsg.style.textAlign = 'right';
  chatBox.appendChild(userMsg);
  input.value = '';

  // Send to backend
  try {
    const response = await fetch('https://bluejay-3999.onrender.com', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, user_id: 'bluejay-user' })
    });

    const data = await response.json();
    const botMsg = document.createElement('div');
    botMsg.textContent = data.reply || 'Sorry, something went wrong.';
    chatBox.appendChild(botMsg);
    chatBox.scrollTop = chatBox.scrollHeight;
  } catch (error) {
    const errorMsg = document.createElement('div');
    errorMsg.textContent = 'Error: Unable to connect to the server.';
    chatBox.appendChild(errorMsg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }
}
