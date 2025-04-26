const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');

// Backend server URL
const SERVER_URL = 'https://pbj-server1.onrender.com/chat';

function appendMessage(content, sender) {
  const message = document.createElement('div');
  message.className = sender === 'user' ? 'user-message' : 'bot-message';
  message.innerText = content;
  chatBox.appendChild(message);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
  const input = userInput.value.trim();
  if (!input) return;

  appendMessage(input, 'user');
  userInput.value = '';

  try {
    const response = await fetch(SERVER_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: input })
    });

    if (!response.ok) {
      appendMessage('Error: Unable to connect to BlueJay.', 'bot');
      return;
    }

    const data = await response.json();
    appendMessage(data.reply || 'No response from BlueJay.', 'bot');
  } catch (error) {
    appendMessage('Error: Connection failed.', 'bot');
  }
}