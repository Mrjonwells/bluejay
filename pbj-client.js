// Generate or retrieve client_id
let clientId = localStorage.getItem("bluejay_client_id");
if (!clientId) {
  clientId = crypto.randomUUID();
  localStorage.setItem("bluejay_client_id", clientId);
}

const submitBtn = document.getElementById("submitBtn");
const userInput = document.getElementById("userInput");
const responseDiv = document.getElementById("response");

submitBtn.addEventListener("click", submitQuestion);

userInput.addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    e.preventDefault();
    submitQuestion();
  }
});

async function submitQuestion() {
  const input = userInput.value.trim();
  if (!input) {
    responseDiv.innerHTML += `<div><em>Please enter a question.</em></div>`;
    return;
  }

  responseDiv.innerHTML += `<div><strong>You:</strong> ${input}</div>`;
  userInput.value = "";
  responseDiv.innerHTML += `<div><em>BlueJay is thinking...</em></div>`;

  try {
    const res = await fetch("https://pbj-server1.onrender.com/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: input,
        client_id: clientId
      }),
    });

    const data = await res.json();
    const reply = data.response || "No response received.";

    // Clear the "thinking" message
    const allLines = responseDiv.innerHTML.split("<div>");
    const filteredLines = allLines.filter(line => !line.includes("BlueJay is thinking..."));
    responseDiv.innerHTML = filteredLines.join("<div>");

    // Show BlueJay's response
    responseDiv.innerHTML += `<div><strong>BlueJay:</strong> ${reply}</div>`;

    // Optionally show savings if returned
    if (data.savings) {
      const savings = data.savings;
      responseDiv.innerHTML += `
        <div style="margin-top: 1rem; padding: 10px; background: #dff0d8; border-radius: 5px;">
          <strong>Estimated Savings:</strong><br />
          Monthly: $${savings.monthly_savings}<br />
          Yearly: $${savings.yearly_savings}
        </div>`;
    }

    responseDiv.scrollTop = responseDiv.scrollHeight;

  } catch (error) {
    responseDiv.innerHTML += `<div><strong>Error:</strong> ${error.message}</div>`;
  }
}
