// chat.js

document.addEventListener('DOMContentLoaded', () => {
  const chatForm = document.getElementById('chat-form');
  const chatInput = document.getElementById('chat-input');
  const chatMessages = document.getElementById('chat-messages');

  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (!message) return;

    appendMessage('user', message);
    chatInput.value = '';
    chatInput.disabled = true;

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });

      const data = await response.json();
      appendMessage('bot', data.reply);
    } catch (error) {
      appendMessage('bot', 'Sorry, something went wrong.');
    } finally {
      chatInput.disabled = false;
      chatInput.focus();
    }
  });

  function appendMessage(sender, text) {
    const messageElem = document.createElement('div');
    messageElem.className = `message ${sender}`;
    messageElem.innerText = text;
    chatMessages.appendChild(messageElem);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
});