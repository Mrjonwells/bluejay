const chatBox = document.getElementById('chatBox');
const userInput = document.getElementById('userInput');

function appendMessage(text, sender) {
  const msg = document.createElement('div');
  msg.className = `message ${sender}`;
  msg.innerText = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  appendMessage(message, 'user');
  userInput.value = '';

  appendMessageTyping();

  fetch('https://bluejay-3999.onrender.com/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, user_id: getUserID() })
  })
    .then(res => res.json())
    .then(data => {
      removeTyping();
      appendMessage(data.reply, 'bot');
    })
    .catch(() => {
      removeTyping();
      appendMessage("Sorry, I couldn’t reach BlueJay right now.", 'bot');
    });
}

function appendMessageTyping() {
  const typing = document.createElement('div');
  typing.className = 'message bot typing-indicator';
  typing.id = 'typing';
  typing.innerHTML = '<span></span><span></span><span></span>';
  chatBox.appendChild(typing);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTyping() {
  const typing = document.getElementById('typing');
  if (typing) typing.remove();
}

function getUserID() {
  let uid = localStorage.getItem('bluejay_uid');
  if (!uid) {
    uid = crypto.randomUUID();
    localStorage.setItem('bluejay_uid', uid);
  }
  return uid;
}

userInput.addEventListener('keydown', e => {
  if (e.key === 'Enter') sendMessage();
});
