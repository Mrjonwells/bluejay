let clientId = localStorage.getItem("bluejay_client_id");
if (!clientId) {
  clientId = crypto.randomUUID();
  localStorage.setItem("bluejay_client_id", clientId);
}

document.getElementById("submitBtn").addEventListener("click", submitQuestion);
document.getElementById("userInput").addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    e.preventDefault();
    submitQuestion();
  }
});

async function submitQuestion() {
  const inputField = document.getElementById("userInput");
  const responseDiv = document.getElementById("response");
  const userInput = inputField.value.trim();

  if (!userInput) {
    responseDiv.innerHTML = "<strong>Please enter a question.</strong>";
    return;
  }

  responseDiv.innerHTML = "<em>BlueJay is thinking...</em>";

  try {
    const res = await fetch("https://pbj-server1.onrender.com/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: userInput,
        client_id: clientId
      }),
    });

    const data = await res.json();
    inputField.value = "";

    let output = `<strong>You:</strong> ${userInput}<br><br><strong>BlueJay:</strong> ${data.response || "No response received."}`;

    if (data.savings) {
      output += "<br><br><strong>Estimated Savings:</strong><br>";
      output += `Monthly: $${data.savings.monthly_savings}<br>`;
      output += `Yearly: $${data.savings.yearly_savings}<br>`;
    }

    responseDiv.innerHTML = output;

  } catch (error) {
    responseDiv.innerHTML = `<strong>Error:</strong> ${error.message}`;
  }
}
