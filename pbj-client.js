document.getElementById('submitBtn').addEventListener('click', async () => {
  const userInput = document.getElementById('userInput').value.trim();
  const responseDiv = document.getElementById('response');
  const savingsDiv = document.getElementById('savings-summary');

  if (!userInput) {
    responseDiv.textContent = "Please enter a question.";
    return;
  }

  responseDiv.textContent = "BlueJay is thinking...";
  savingsDiv.style.display = 'none';
  savingsDiv.textContent = "";

  try {
    const clientId = localStorage.getItem('client_id') || crypto.randomUUID();
    localStorage.setItem('client_id', clientId);

    const res = await fetch("https://pbj-server1.onrender.com/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userInput, client_id: clientId })
    });

    const data = await res.json();
    responseDiv.textContent = data.response || "No response received.";

    // Show savings if returned from backend
    if (data.savings) {
      let summary = "";
      if (data.savings.monthly) {
        summary += `Monthly Savings: $${data.savings.monthly.toFixed(2)}\n`;
      }
      if (data.savings.yearly) {
        summary += `Yearly Savings: $${data.savings.yearly.toFixed(2)}`;
      }
      savingsDiv.textContent = summary;
      savingsDiv.style.display = 'block';
    }

    document.getElementById('userInput').value = "";
  } catch (error) {
    responseDiv.textContent = "Error: " + error.message;
  }
});
