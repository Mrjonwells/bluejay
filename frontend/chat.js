document.addEventListener('DOMContentLoaded', function () {
  const inputField = document.getElementById('user-input');
  const sendButton = document.getElementById('send-button');
  const chatContainer = document.getElementById('chat-container');

  function appendMessage(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.innerText = message;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  function showThinkingDots() {
    const dots = document.createElement('div');
    dots.classList.add('message', 'bot', 'thinking-indicator');
    dots.innerText = 'BlueJay is typing...';
    dots.id = 'thinking-dots';
    chatContainer.appendChild(dots);
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  function removeThinkingDots() {
    const dots = document.getElementById('thinking-dots');
    if (dots) dots.remove();
  }

  async function sendMessage() {
    const userInput = inputField.value.trim();
    if (!userInput) return;

    appendMessage(userInput, 'user');
    inputField.value = '';
    showThinkingDots();

    try {
      const response = await fetch('https://bluejay-3999.onrender.com/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userInput })
      });

      const data = await response.json();
      removeThinkingDots();

      if (data && data.response) {
        appendMessage(data.response, 'bot');
      } else {
        appendMessage('Oops! No response received.', 'bot');
      }
    } catch (error) {
      removeThinkingDots();
      appendMessage('Oops! Something went wrong.', 'bot');
    }
  }

  sendButton.addEventListener('click', sendMessage);

  inputField.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') sendMessage();
  });
});
