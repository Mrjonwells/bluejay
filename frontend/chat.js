const chatContainer = document.getElementById('chat-container');
const chatBox = document.getElementById('chat-box');
const chatInput = document.getElementById('chat-input');

let threadId = null;

function addMessage(text, sender) {
  const message = document.createElement('div');
  message.className = `message ${sender}`;
  message.innerText = text;
  chatBox.appendChild(message);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function showTyping() {
  const typing = document.createElement('div');
  typing.className = 'message assistant typing';
  typing.innerHTML = `<span class="dot"></span><span class="dot"></span><span class="dot"></span>`;
  typing.id = 'typing-indicator';
  chatBox.appendChild(typing);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function hideTyping() {
  const typing = document.getElementById('typing-indicator');
  if (typing) typing.remove();
}

async function sendMessage() {
  const userInput = chatInput.value.trim();
  if (!userInput) return;

  addMessage(userInput, 'user');
  chatInput.value = '';
  showTyping();

  try {
    const response = await fetch('https://bluejay-api.onrender.com/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userInput, thread_id: threadId }),
    });

    const data = await response.json();
    threadId = data.thread_id;
    hideTyping();
    addMessage(data.response, 'assistant');
  } catch (err) {
    hideTyping();
    addMessage('Something went wrong. Try again later.', 'assistant');
  }
}

chatInput.addEventListener('keydown', function (e) {
  if (e.key === 'Enter') {
    sendMessage();
  }
});

// initial greeting
window.onload = () => {
  setTimeout(() => {
    addMessage("Hi, I'm BlueJay — your business expert. What’s your name?", 'assistant');
  }, 300);
};