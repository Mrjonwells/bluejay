const chatBox = document.getElementById('chat-box');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');

function addMessage(message, sender = 'user') {
  const div = document.createElement('div');
  div.textContent = message;
  div.className = sender;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage(e) {
  e.preventDefault();
  const message = userInput.value.trim();
  if (!message) return;
  addMessage(message, 'user');
  userInput.value = '';

  try {
    const response = await fetch('https://bluejay-39999.onrender.com/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });
    const data = await response.json();
    addMessage(data.reply, 'bot');
  } catch (err) {
    addMessage('Something went wrong. Please try again.', 'bot');
  }
}

chatForm.addEventListener('submit', sendMessage);
