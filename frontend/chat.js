const backendUrl = 'https://pbj-server1.onrender.com';
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const chatMessages = document.getElementById('chat-messages');

let userId = localStorage.getItem('user_id');
if (!userId) {
  userId = crypto.randomUUID();
  localStorage.setItem('user_id', userId);
}

function appendMessage(sender, message) {
  const msg = document.createElement('div');
  msg.innerHTML = `<strong>${sender}:</strong> ${message}`;
  chatMessages.appendChild(msg);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

chatForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const userMessage = chatInput.value.trim();
  if (!userMessage) return;

  appendMessage('You', userMessage);
  chatInput.value = '';

  try {
    const response = await fetch(`${backendUrl}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, message: userMessage })
    });

    const data = await response.json();
    appendMessage('BlueJay', data.reply);
  } catch (error) {
    appendMessage('Error', 'There was a problem connecting to BlueJay.');
    console.error(error);
  }
});