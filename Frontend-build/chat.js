document.addEventListener('DOMContentLoaded', () => {
  const chatForm = document.getElementById('chat-form');
  const chatInput = document.getElementById('chat-input');
  const chatBox = document.getElementById('chat-box');

  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const userMessage = chatInput.value.trim();
    if (!userMessage) return;

    // Display user's message
    appendMessage('user', userMessage);
    chatInput.value = '';

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userMessage })
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.statusText}`);
      }

      const data = await response.json();
      appendMessage('assistant', data.reply);
    } catch (error) {
      console.error('Error:', error);
      appendMessage('assistant', 'Sorry, there was an error processing your message.');
    }
  });

  function appendMessage(sender, message) {
    const messageElem = document.createElement('div');
    messageElem.className = `message ${sender}`;
    messageElem.textContent = message;
    chatBox.appendChild(messageElem);
    chatBox.scrollTop = chatBox.scrollHeight;
  }
});
