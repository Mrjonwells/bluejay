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

  const typing = document.createElement('div');
  typing.className = 'typing-indicator';
  typing.id = 'typing';
  typing.innerHTML = '<span></span><span></span><span></span>';
  chatBox.appendChild(typing);
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const response = await fetch('https://bluejay-3999.onrender.com/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, user_id: 'bluejay-user' })
    });

    const data = await response.json();
    typing.remove();

    const botMsg = document.createElement('div');
    botMsg.textContent = data.reply || 'Sorry, something went wrong.';
    chatBox.appendChild(botMsg);
    chatBox.scrollTop = chatBox.scrollHeight;
  } catch (error) {
    typing.remove();

    const errorMsg = document.createElement('div');
    errorMsg.textContent = 'Error: Unable to connect to the server.';
    chatBox.appendChild(errorMsg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('userInput').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') sendMessage();
  });
});