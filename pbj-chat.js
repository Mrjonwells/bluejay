const chatLog = document.getElementById('chatLog');
const sendBtn = document.getElementById('sendBtn');
const userInput = document.getElementById('userInput');

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') sendMessage();
});

function getThreadData() {
  const stored = JSON.parse(localStorage.getItem('bluejay_thread') || '{}');
  const now = Date.now();
  if (stored.id && stored.timestamp && now - stored.timestamp < 20 * 60 * 1000) {
    return stored;
  }
  return { id: null, timestamp: now };
}

function setThreadData(id) {
  localStorage.setItem('bluejay_thread', JSON.stringify({
    id,
    timestamp: Date.now()
  }));
}

function appendMessage(role, text = "") {
  const div = document.createElement('div');
  div.className = `message ${role}`;
  div.innerHTML = text;
  chatLog.appendChild(div);
  chatLog.scrollTop = chatLog.scrollHeight;
  return div;
}

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  userInput.value = '';
  userInput.disabled = true;
  appendMessage('user', message);
  const botMsg = appendMessage('bot', "BlueJay is thinking...");

  const threadData = getThreadData();

  try {
    const res = await fetch('https://pbj-server1.onrender.com/pbj', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message,
        thread_id: threadData.id
      })
    });

    const data = await res.json();

    if (data.thread_id && data.thread_id !== threadData.id) {
      setThreadData(data.thread_id);
    }

    botMsg.innerHTML = data.response || "No response received.";
    chatLog.scrollTop = chatLog.scrollHeight;
  } catch (err) {
    botMsg.innerHTML = "Error: " + err.message;
  }

  userInput.disabled = false;
  userInput.focus();
}
