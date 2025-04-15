document.getElementById('submitBtn').addEventListener('click', sendMessage);
document.getElementById('userInput').addEventListener('keypress', (e) => {
  if (e.key === 'Enter') sendMessage();
});

async function sendMessage() {
  const inputEl = document.getElementById('userInput');
  const responseDiv = document.getElementById('response');
  const message = inputEl.value.trim();

  if (!message) return;

  inputEl.disabled = true;
  responseDiv.textContent = "BlueJay is thinking...";

  const threadData = getThreadData();
  const payload = {
    message,
    thread_id: threadData.id
  };

  try {
    const res = await fetch('https://pbj-server1.onrender.com/pbj', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (data.thread_id && data.thread_id !== threadData.id) {
      setThreadData(data.thread_id);
    }

    responseDiv.textContent = data.response || "No response.";
  } catch (err) {
    responseDiv.textContent = "Error: " + err.message;
  }

  inputEl.value = "";
  inputEl.disabled = false;
  inputEl.focus();
}

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
