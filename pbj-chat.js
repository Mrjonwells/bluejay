document.getElementById('submitBtn').addEventListener('click', sendMessage);
document.getElementById('userInput').addEventListener('keypress', (e) => {
  if (e.key === 'Enter') sendMessage();
});

async function sendMessage() {
  const inputEl = document.getElementById('userInput');
  const responseDiv = document.getElementById('response');
  const message = inputEl.value.trim();

  if (!message) {
    responseDiv.textContent = "Please enter a message.";
    return;
  }

  inputEl.disabled = true;
  responseDiv.textContent = "BlueJay is thinking";
  responseDiv.classList.add("thinking");

  try {
    const res = await fetch('https://pbj-server1.onrender.com/pbj', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    const data = await res.json();
    responseDiv.classList.remove("thinking");
    responseDiv.textContent = data.response || "No response received.";
  } catch (err) {
    responseDiv.classList.remove("thinking");
    responseDiv.textContent = "Error: " + err.message;
  } finally {
    inputEl.value = "";
    inputEl.disabled = false;
    inputEl.focus();
  }
}
