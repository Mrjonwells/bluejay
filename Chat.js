document.getElementById('submitBtn').addEventListener('click', async () => {
  const userInput = document.getElementById('userInput').value.trim();
  const responseDiv = document.getElementById('response');
  if (!userInput) return;

  responseDiv.innerHTML += `<div class="message user"><strong>You:</strong> ${userInput}</div>`;
  document.getElementById('userInput').value = '';
  responseDiv.innerHTML += `<div class="message bot">BlueJay is thinking...</div>`;

  try {
    const res = await fetch("https://pbj-server1.onrender.com/pbj", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userInput }),
    });

    const data = await res.json();
    const botMessage = data.response || "No response.";
    responseDiv.innerHTML += `<div class="message bot"><strong>BlueJay:</strong> ${botMessage}</div>`;
    responseDiv.scrollTop = responseDiv.scrollHeight;
  } catch (error) {
    responseDiv.innerHTML += `<div class="message bot">Error: ${error.message}</div>`;
  }
});

document.getElementById('userInput').addEventListener('keypress', function (e) {
  if (e.key === 'Enter') document.getElementById('submitBtn').click();
});
