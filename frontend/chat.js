document.addEventListener('DOMContentLoaded', function () {
  const inputField = document.getElementById('user-input');
  const sendButton = document.getElementById('send-button');
  const chatContainer = document.getElementById('chat-container');
  const typingIndicator = document.getElementById('typing-indicator');

  function appendMessage(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.innerText = message;
    chatContainer.insertBefore(messageDiv, typingIndicator);
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  async function sendMessage() {
    const userInput = inputField.value.trim();
    if (!userInput) return;

    appendMessage(userInput, 'user');
    inputField.value = '';
    typingIndicator.style.display = 'flex';
    chatContainer.scrollTop = chatContainer.scrollHeight;

    try {
      const response = await fetch('https://bluejay-3999.onrender.com/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userInput })
      });

      const data = await response.json();
      if (data && data.response) {
        appendMessage(data.response, 'bot');
      } else {
        appendMessage('Sorry, no response received.', 'bot');
      }
    } catch (error) {
      appendMessage('Oops! Something went wrong.', 'bot');
    } finally {
      typingIndicator.style.display = 'none';
    }
  }

  sendButton.addEventListener('click', sendMessage);
  inputField.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') sendMessage();
  });
});
