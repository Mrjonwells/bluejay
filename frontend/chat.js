document.addEventListener('DOMContentLoaded', function () {
  const inputField = document.getElementById('user-input');
  const sendButton = document.getElementById('send-button');
  const chatContainer = document.getElementById('chat-container');
  const thinkingIcon = document.getElementById('thinking-icon');

  function appendMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.innerText = text;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  async function sendMessage() {
    const userInput = inputField.value.trim();
    if (!userInput) return;

    appendMessage(userInput, 'user');
    inputField.value = '';
    thinkingIcon.style.display = 'block';

    try {
      const response = await fetch('https://bluejay-3999.onrender.com/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userInput })
      });

      const data = await response.json();
      if (data && data.response) {
        appendMessage(data.response, 'bot');
      }
    } catch (error) {
      appendMessage('Oops! Something went wrong.', 'bot');
    } finally {
      thinkingIcon.style.display = 'none';
    }
  }

  sendButton.addEventListener('click', sendMessage);
  inputField.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') sendMessage();
  });
});
