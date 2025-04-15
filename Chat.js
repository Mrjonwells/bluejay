document.getElementById('submitBtn').addEventListener('click', async () => {
  const userInput = document.getElementById('userInput').value.trim();
  const responseDiv = document.getElementById('response');
  if (!userInput) return;

  // Add user message
  const userMsg = document.createElement('div');
  userMsg.classList.add('message', 'user');
  userMsg.innerHTML = `<strong>You:</strong> ${userInput}`;
  responseDiv.appendChild(userMsg);
  document.getElementById('userInput').value = '';

  // Add thinking animation
  const botThinking = document.createElement('div');
  botThinking.classList.add('message', 'bot');
  botThinking.textContent = 'BlueJay is thinking...';
  responseDiv.appendChild(botThinking);
  responseDiv.scrollTop = responseDiv.scrollHeight;

  try {
    const res = await fetch("https://pbj-server1.onrender.com/pbj", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userInput }),
    });

    const data = await res.json();
    const botMessage = data.response || "No response.";

    // Replace thinking with actual response
    botThinking.innerHTML = `<strong>BlueJay:</strong> ${botMessage}`;
    responseDiv.scrollTop = responseDiv.scrollHeight;

  } catch (error) {
    botThinking.textContent = `Error: ${error.message}`;
  }
});

document.getElementById('userInput').addEventListener('keypress', function (e) {
  if (e.key === 'Enter') document.getElementById('submitBtn').click();
});
