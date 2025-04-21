document.getElementById('submitBtn').addEventListener('click', submitQuestion);
document.getElementById('userInput').addEventListener('keypress', function (e) {
  if (e.key === 'Enter') {
    submitQuestion();
  }
});

async function submitQuestion() {
  const userInput = document.getElementById('userInput').value.trim();
  const responseDiv = document.getElementById('response');
  const savingsDiv = document.getElementById('savingsBox');

  if (!userInput) {
    responseDiv.innerHTML += "<div class='bot'>Please enter a question.</div>";
    return;
  }

  responseDiv.innerHTML += `<div class='user'><strong>You:</strong> ${userInput}</div>`;
  responseDiv.innerHTML += "<div class='bot'><em>BlueJay is thinking...</em></div>";
  document.getElementById('userInput').value = '';

  const client_id = localStorage.getItem('pbj_client_id') || crypto.randomUUID();
  localStorage.setItem('pbj_client_id', client_id);

  try {
    const res = await fetch('https://pbj-server1.onrender.com/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userInput, client_id })
    });

    const data = await res.json();
    const reply = data.response || "No response received.";

    // Remove old "thinking..." message
    const allBotResponses = document.querySelectorAll('.bot');
    if (allBotResponses.length) {
      allBotResponses[allBotResponses.length - 1].remove();
    }

    responseDiv.innerHTML += `<div class='bot'><strong>BlueJay:</strong> ${reply}</div>`;

    // Show savings data if returned
    if (data.savings) {
      savingsDiv.innerHTML = `
        <h3>Estimated Savings</h3>
        <p><strong>Monthly:</strong> $${data.savings.monthly_savings}</p>
        <p><strong>Yearly:</strong> $${data.savings.yearly_savings}</p>
      `;
    }

    responseDiv.scrollTop = responseDiv.scrollHeight;
  } catch (error) {
    responseDiv.innerHTML += `<div class='bot'>Error: ${error.message}</div>`;
  }
}
