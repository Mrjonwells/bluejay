const chatLog = document.getElementById('chatLog');
const sendBtn = document.getElementById('sendBtn');
const userInput = document.getElementById('userInput');

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') sendMessage();
});

// Get or expire the current thread_id from localStorage
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

// Add a chat message to the UI
function appendMessage(role, text = "") {
  const div = document.createElement('div');
  div.className = `message ${role}`;
  div.innerHTML = text; // Render inline HTML safely (be cautious with inputs!)
  chatLog.appendChild(div);
  chatLog.scrollTop = chatLog.scrollHeight;
  return div;
}

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  userInput.value = '';
  userInput.disabled = true;
  const userMsg = appendMessage('user', message);
  const botMsg = appendMessage('bot', "");

  const threadData = getThreadData();

  const eventSource = new EventSourcePolyfill('https://pbj-server1.onrender.com/pbj', {
    headers: { 'Content-Type': 'application/json' },
    payload: JSON.stringify({
      message,
      thread_id: threadData.id
    }),
    method: 'POST'
  });

  let fullBotReply = "";

  eventSource.onmessage = function (event) {
    if (event.data.startsWith('<END>|')) {
      const newThread = event.data.split('|')[1];
      if (newThread && newThread !== threadData.id) {
        setThreadData(newThread);
      }
      eventSource.close();
      userInput.disabled = false;
      userInput.focus();
    } else {
      fullBotReply += event.data;
      botMsg.innerHTML = fullBotReply;
      chatLog.scrollTop = chatLog.scrollHeight;
    }
  };

  eventSource.onerror = function (err) {
    botMsg.textContent = "Error: Could not receive response.";
    console.error("Streaming error:", err);
    eventSource.close();
    userInput.disabled = false;
  };
}
