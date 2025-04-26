const backendUrl = "https://bluejay-1.onrender.com"; // Updated backend address

document.getElementById('sendButton').addEventListener('click', sendMessage);
document.getElementById('userInput').addEventListener('keypress', function (e) {
  if (e.key === 'Enter') {
    sendMessage();
  }
});

function addMessage(message, className) {
  const chatContainer = document.getElementById('chatContainer');
  const messageElement = document.createElement('div');
  messageElement.className = className;
  messageElement.textContent = message;
  chatContainer.appendChild(messageElement);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function sendMessage() {
  const userInput = document.getElementById('userInput');
  const message = userInput.value.trim();
  if (message === '') return;

  addMessage(message, 'user-message');
  userInput.value = '';

  try {
    const response = await fetch(`${backendUrl}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: message }),
    });

    if (!response.ok) {
      throw new Error('Server error');
    }

    const data = await response.json();
    addMessage(data.response, 'bot-message');
  } catch (error) {
    console.error('Error sending message:', error);
    addMessage('Error connecting to server.', 'error-message');
  }
}